from __future__ import print_function
import os
import sys
import logging
import exifread
import piexif
import json
import secrets
import arrow
import boto3
import shutil
from botocore.exceptions import BotoCoreError, ClientError
from fractions import Fraction

from app import models, database, db_functions, blurring_functions

from googleapiclient.http import MediaFileUpload
from starlette.staticfiles import StaticFiles
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime
from sqlalchemy.orm import Session
from dateutil import tz
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Set up logging
logging.getLogger("myapp")

models.database.Base.metadata.create_all(bind=database.engine)

# S3 access info for copying images to WebCOOS
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_DEFAULT_REGION")
)
s3_bucket = os.environ.get("S3_BUCKET_NAME")


description = """
Sunny Day Flooding Project Photo API lets you:

* **Upload pictures**
* **Get info about latest pictures**
* **Add new camera sites**
* **View existing camera sites**
"""

app = FastAPI(
    title="Sunny Day Flooding Project Photo API",
    description=description,
    version="0.1.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Adam Gold",
        "url": "https://tarheels.live/sunnydayflood/people/",
        "email": "gold@unc.edu",
    },
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)

security = HTTPBasic()

app.mount("/public", StaticFiles(directory="/photo_storage"), name="photo_storage")

host_os = os.getenv("HOST_OS")
if host_os and host_os.lower() == "windows":
    # for local running only below
    fp = open("/code/app/auth.json")  
    json_secret = fp.read()
    fp.close()
    json_secret = json.loads(json_secret)
    json_secret["private_key"] = json_secret["private_key"].replace("\\n", "\n")
else:
    # The line below is for OpenShift running
    json_secret = json.loads(os.environ.get('GOOGLE_JSON_KEY'))


google_drive_folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

scope = ["https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict=json_secret, scopes=scope)

# setup the google drive stance and sign in
drive = build('drive', 'v3', credentials=credentials)


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to convert decimal degrees to DMS in EXIF rational format
def deg_to_dms_rational(deg):
    """Convert decimal degrees to degrees, minutes, seconds in EXIF rational format."""
    d = int(deg)
    m_float = abs(deg - d) * 60
    m = int(m_float)
    s = (m_float - m) * 60
    return [
        (abs(d), 1),
        (m, 1),
        (int(s * 10000), 10000)
    ]

def set_gps_location(file_path, output_path, lat, lon):
    # Open image and get current EXIF
    img = Image.open(file_path)
    exif_dict = piexif.load(img.info.get('exif', b''))

    # Define GPS IFD
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: deg_to_dms_rational(lat),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if lon >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: deg_to_dms_rational(lon),
    }

    # Add GPS IFD to EXIF and insert back
    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)

    # Save image with updated EXIF
    img.save(output_path, exif=exif_bytes)

def get_or_create_folder(drive, parent_id, folder_name):
    """Find or create a google drive folder by name within a parent folder.
    Args:
        drive: Google Drive service object
        parent_id: ID of the parent folder
        folder_name: Name of the folder to find or create
    Returns:
        ID of the folder (existing or newly created)
    """
    # Search for the folder
    folder_info = drive.files().list(
        corpora="drive",
        driveId=google_drive_folder_id,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q="name='" + folder_name + "' and mimeType='application/vnd.google-apps.folder' and '" + parent_id + "' in parents and trashed = false"
    ).execute().get('files', [])
    
    # If folder exists, return its ID
    if len(folder_info) > 0:
        return folder_info[0].get('id')
    
    # If folder doesn't exist, create it
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    file = drive.files().create(body=file_metadata,
                                supportsAllDrives=True).execute()
    return file.get('id')

def file_exists_in_drive(drive, parent_id, filename):
    """Check if a file exists in a Google Drive folder.
    Args:
        drive: Google Drive service object
        parent_id: ID of the parent folder
        filename: Name of the file to search for
    Returns:
        True if file exists, False otherwise
    """
    file_info = drive.files().list(
        corpora="drive",
        driveId=google_drive_folder_id,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q="'" + parent_id + "'" + " in parents and trashed = false and name='" + filename + "'"
    ).execute().get('files', [])
    return len(file_info) > 0

def upload_file_to_drive(drive, parent_id, filename, local_path):
    """Upload a file to Google Drive if it doesn't already exist.
    Args:
        drive: Google Drive service object
        parent_id: ID of the parent folder
        filename: Name for the file on Drive
        local_path: Local path to the file to upload
    """
    if not file_exists_in_drive(drive, parent_id, filename):
        file_metadata = {
            'name': filename,
            'parents': [parent_id]
        }
        media = MediaFileUpload(local_path,
                                mimetype='image/jpg',
                                resumable=True)
        drive.files().create(body=file_metadata,
                            media_body=media,
                            supportsAllDrives=True).execute()
    else:
        logging.info("Picture already exists! Not overwriting")


@app.get("/")
async def root():
    return {"message": "Hello there! Navigate to https://photos-sunnydayflood.apps.cloudapps.unc.edu/docs to view the documentation for this API"}


@app.post('/upload_picture')
async def _file_upload(
        file: UploadFile = File(...),
        camera_ID: str = Form(..., example="CAM_BF_01"),
        timezone: str = Form("EST"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    logging.info("/upload_picture " + camera_ID + " " + file.filename)

    # Authenticate
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Save the original high-res image to photo_storage (will be deleted later)
    original_pic_path = "/photo_storage/highres_" + camera_ID + ".jpg"
    with open(original_pic_path, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()

    # Get the lat/lon and insert into EXIF of the original high-res image
    camera_info = db_functions.get_camera( db=db, camera_ID=camera_ID)
    if not camera_info:
        return {"ERROR": "Camera ID "+camera_ID+" not found in database"}
    lat = camera_info[0].lat
    lon = camera_info[0].lng
    set_gps_location(original_pic_path, original_pic_path, lat, lon)

    # Extract the DateTimeOriginal from the original image's EXIF data
    with Image.open(original_pic_path) as img:
        exif_bytes = img.info.get('exif')
        exif_dict = piexif.load(exif_bytes) if exif_bytes else {}
    datetime_bytes = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
    if not datetime_bytes:
        raise ValueError("DateTimeOriginal tag not found in EXIF data.")
    datetime_string = datetime_bytes.decode("utf-8")    # Decode bytes to string
    # Convert the DateTimeOriginal to a timezone-aware Arrow object in UTC
    datetime_original_arrow = arrow.get(datetime.strptime(datetime_string, "%Y:%m:%d %H:%M:%S"),
                                        tz.gettz(timezone)).to('utc')
    picture_label = camera_ID + "_" + datetime_original_arrow.format("YYYYMMDDHHmmss") + ".jpg"     # Label for the picture file, which includes the camera ID and the timestamp
    date_label = datetime_original_arrow.format("YYYY-MM-DD")   # Label for the date folder, which is just the date portion of the timestamp

    # Create a reduced-size version of the image for blurring and uploading to Google Drive and S3
    try:
        img = Image.open(original_pic_path)
    except OSError:
        return "Error opening image. Image is corrupt"
    except:
        return "Error opening image. Unknown error"
    img.thumbnail(size=(1000, 750))
    reduced_image_path = "/photo_storage/" + camera_ID + ".jpg"
    img.save(reduced_image_path, exif=exif_bytes)
    img.close()

    # Find or create folder hierarchy on Google Drive
    images_folder_id = drive.files().list(
        corpora="drive",
        driveId=google_drive_folder_id,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q="name='Images' and mimeType='application/vnd.google-apps.folder'"
    ).execute().get('files')[0].get('id')
    camera_image_folder_id = get_or_create_folder(drive, images_folder_id, camera_ID)
    date_folder_id = get_or_create_folder(drive, camera_image_folder_id, date_label)
    upload_file_to_drive(drive, date_folder_id, picture_label, original_pic_path)    # Upload the file if it doesn't already exist

    # Remove previous timestamped photo if exists
    previous_pic = db_functions.get_latest_photo_info(db=db, camera_ID=camera_ID)
    try:
        os.remove("/photo_storage/" + previous_pic.drive_filename)
    except:
        logging.info("File not found")

    # write the info for the current photo to the database
    db_functions.write_photo_info(
        db=db,
        drive_filename=picture_label,
        camera_ID=camera_ID,
        FileSize=os.path.getsize(original_pic_path),
        DateTimeOriginal=datetime_string,
        original_tz=timezone,
        DateTimeOriginalUTC=datetime_original_arrow.datetime
    )

    # Apply the blurring function to the reduced image
    blurring_functions.blur_image(camera_ID.replace("CAM_", ""), reduced_image_path)
    destination_path = os.path.join("/photo_storage", picture_label)
    try:
        shutil.copy2(reduced_image_path, destination_path)
    except OSError as exc:
        logging.error("Failed to copy reduced image to %s: %s", destination_path, exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to save reduced image")
    
    # Generate the S3 'slug' for the image
    place_name = camera_info[0].place.split(',')[0] if ',' in camera_info[0].place else camera_info[0].place
    place_name = place_name.replace(" ", "_").lower() + "_" + camera_ID.rsplit('_', 1)[-1]
    if camera_info[0].sendto_webcoos is True:
        # Copy blurred image to S3 bucket
        # Construct the S3 path using EXIF date and camera_ID
        s3_folder_path = f"media/sources/webcoos/groups/ncsu/assets/{place_name}/feeds/raw-video-data/products/image-stills/elements/{datetime_original_arrow.format('YYYY/MM/DD')}"
        s3_filename = f"{camera_ID}-{datetime_original_arrow.format('YYYY-MM-DD-HHmmss')}Z.jpg"
        s3_key = f"{s3_folder_path}/{s3_filename}"

        logging.info(f"Uploading to S3: {s3_key}")

        # Upload the image to S3
        try:
            with open(reduced_image_path, "rb") as f:
                s3_client.upload_fileobj(f, s3_bucket, s3_key)
            logging.info("Upload successful.")
        except (BotoCoreError, ClientError) as e:
            logging.info(f"Upload failed: {e}")

    # Remove the original high-res image leaving the reduced blurred version
    os.remove(original_pic_path)

    return {"SUCCESS!"}


@app.post('/upload_overlay')
async def _overlay_upload(
        file: UploadFile = File(...),
        camera_ID: str = Form(..., example="CAM_BF_01"),
        timezone: str = Form("EST"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    logging.info("/upload_overlay " + camera_ID + " " + file.filename)

    # Authenticate
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # save highres version to photo_storage (will be deleted later)
    original_pic_path = "/photo_storage/highresOverlay_" + camera_ID + ".jpg"
    with open(original_pic_path, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()

    # Extract the DateTimeOriginal from the original image's EXIF data
    with Image.open(original_pic_path) as img:
        exif_bytes = img.info.get('exif')
        exif_dict = piexif.load(exif_bytes) if exif_bytes else {}
    datetime_bytes = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
    if not datetime_bytes:
        raise ValueError("DateTimeOriginal tag not found in EXIF data.")
    datetime_string = datetime_bytes.decode("utf-8")    # Decode bytes to string
    # Convert the DateTimeOriginal to a timezone-aware Arrow object in UTC
    datetime_original_arrow = arrow.get(datetime.strptime(datetime_string, "%Y:%m:%d %H:%M:%S"),
                                        tz.gettz(timezone)).to('utc')
    picture_label = camera_ID + "_" + datetime_original_arrow.format("YYYYMMDDHHmmss") + ".jpg"     # Label for the picture file, which includes the camera ID and the timestamp

    # Create a reduced-size version of the image for blurring and serving via the web
    try:
        img = Image.open(original_pic_path)
    except OSError:
        return "Error opening image. Image is corrupt"
    except:
        return "Error opening image. Unknown error"
    img.thumbnail(size=(1000, 750))
    reduced_image_path = "/photo_storage/segmap_overlay_" + camera_ID + ".jpg"
    img.save(reduced_image_path, exif=exif_bytes)
    img.close()

    # Remove previous timestamped photo if exists
    previous_pic = db_functions.get_latest_photo_info(db=db, camera_ID=camera_ID)
    try:
        os.remove("/photo_storage/segmap_overlay_" + previous_pic.drive_filename)
    except:
        logging.info("File not found")


    blurring_functions.blur_image(camera_ID.replace("CAM_", ""), reduced_image_path)
    # Copy blurred image to filename with timestamp included
    destination_path = os.path.join("/photo_storage", "segmap_overlay_" + picture_label)
    try:
        shutil.copy2(reduced_image_path, destination_path)
    except OSError as exc:
        logging.error("Failed to copy overlay image to %s: %s", destination_path, exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to save overlay image")

    os.remove(original_pic_path)

    return {"SUCCESS!"}


@app.get('/get_latest_picture_info')
def get_latest_picture_info(
        camera_ID: str = Query(..., description="Example: CAM_BF_01"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))
    ro_username = secrets.compare_digest(credentials.username, os.environ.get('ro_username'))
    ro_password = secrets.compare_digest(credentials.password, os.environ.get('ro_password'))

    if not ((correct_username and correct_password) or (ro_username and ro_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    some_photo_info = db_functions.get_latest_photo_info(db=db, camera_ID=camera_ID)

    return {
        some_photo_info
    }


@app.get('/get_picture_info')
def get_picture_info(
        drive_filename: str = Query(..., description="Example: CAM_CB_02_20260514233602.jpg"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))
    ro_username = secrets.compare_digest(credentials.username, os.environ.get('ro_username'))
    ro_password = secrets.compare_digest(credentials.password, os.environ.get('ro_password'))

    if not ((correct_username and correct_password) or (ro_username and ro_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    some_photo_info = db_functions.get_photo_info(db=db, drive_filename=drive_filename)

    if not some_photo_info:
        raise HTTPException(status_code=404, detail="Photo not found")

    return {
        some_photo_info
    }


@app.post('/write_camera')
def add_a_new_camera_site(
        place: str = Query(..., description="Example: Beaufort, North Carolina"),
        camera_ID: str = Query(..., description="Example: CAM_BF_01"),
        lng: float = Query(..., description="Example: -76.3"),
        lat: float = Query(..., description="Example: 34.1"),
        camera_label: str = Query(default=None, description="Example: Front Street"),
        sensor_ID: str = Query(default=None, description="Sensor ID to pull flood status from. Example: BF_01"),
        sendto_webcoos: bool = Query(default=False, description="True to send to WebCOOS, False to not send"),
        doPoseidon: bool = Query(default=False, description="True to enable Poseidon ML processing, False to not enable"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    camera_info = db_functions.add_camera(db=db, place=place, camera_ID=camera_ID, lng=lng, lat=lat, 
                                          camera_label=camera_label, sensor_ID=sensor_ID, 
                                          sendto_webcoos=sendto_webcoos, doPoseidon=doPoseidon)

    return {
        camera_info
    }


@app.get('/get_cameras')
def get_cameras(
        camera_ID: str = Query("all", description="Example: CAM_BF_01"),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))
    ro_username = secrets.compare_digest(credentials.username, os.environ.get('ro_username'))
    ro_password = secrets.compare_digest(credentials.password, os.environ.get('ro_password'))

    if not ((correct_username and correct_password) or (ro_username and ro_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if camera_ID == "all":
        return db_functions.get_all_cameras(
            db=db
        )

    return db_functions.get_camera(
        db=db,
        camera_ID=camera_ID
    )