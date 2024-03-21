from __future__ import print_function
import os
import exifread
import json
import secrets
import arrow

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

models.database.Base.metadata.create_all(bind=database.engine)

# from app import environment_vars
# environment_vars.set_env_vars()

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
    correct_username = secrets.compare_digest(credentials.username, os.environ.get('username'))
    correct_password = secrets.compare_digest(credentials.password, os.environ.get('password'))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    original_pic_path = "/photo_storage/highres_" + camera_ID + ".jpg"
    # original_pic_path = "app/original_pictures/highres_" + camera_ID + ".jpg"

    # SAVE FILE ORIGINAL
    with open(original_pic_path, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()

    img_for_exif = open(original_pic_path, 'rb')
    tags = exifread.process_file(img_for_exif)

    datetime_string = [str(value) for key, value in tags.items() if 'DateTime' in key][0]

    datetime_original_arrow = arrow.get(datetime.strptime(datetime_string, "%Y:%m:%d %H:%M:%S"),
                                        tz.gettz(timezone)).to('utc')

    picture_label = camera_ID + "_" + datetime_original_arrow.format("YYYYMMDDHHmmss") + ".jpg"
    date_label = datetime_original_arrow.format("YYYY-MM-DD")

    try:
        img = Image.open(original_pic_path)
    except OSError:
        return "Error opening image. Image is corrupt"
    except:
        return "Error opening image. Unknown error"

    img.thumbnail(size=(1000, 750))
    reduced_image_path = "/photo_storage/" + camera_ID + ".jpg"
    img.save(reduced_image_path)
    img.close()

    # Find the ID of the "Images" main folder so we can make a new
    # folder for the camera_ID, if needed
    images_folder_id = drive.files().list(
        corpora="drive",
        driveId=google_drive_folder_id,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q="name='Images' and mimeType='application/vnd.google-apps.folder'"
    ).execute().get('files')[0].get('id')

    # Search for the camera's folder within
    camera_image_folder_info = drive.files().list(
        corpora="drive",
        driveId=google_drive_folder_id,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q="name='" + camera_ID + "' and mimeType='application/vnd.google-apps.folder' and '" + images_folder_id + "' in parents and trashed = false"
    ).execute().get('files', [])

    # If the camera's folder exists, get the ID
    if len(camera_image_folder_info) > 0:
        camera_image_folder_id = camera_image_folder_info[0].get('id')

    # If the camera's folder does NOT exist, make it within the "Images" folder and get its ID
    if len(camera_image_folder_info) == 0:
        file_metadata = {
            'name': camera_ID,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [images_folder_id]
        }

        file = drive.files().create(body=file_metadata,
                                    supportsAllDrives=True).execute()

        camera_image_folder_id = file.get('id')

    # Within the camera's folder, see if there is a folder for the specific date of interest (date_label)
    date_folder_info = drive.files().list(
        corpora="drive",
        driveId=google_drive_folder_id,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q="'" + camera_image_folder_id + "'" + " in parents and trashed = false and name='" + date_label + "' and mimeType='application/vnd.google-apps.folder'"
    ).execute().get('files', [])

    # If there is a folder for the date within the camera's folder, get the ID
    if len(date_folder_info) > 0:
        date_folder_id = date_folder_info[0].get('id')

    # If there is NOT a folder for the date within the camera's folder, make one within that folder
    if len(date_folder_info) == 0:
        # make new folder for the date

        file_metadata = {
            'name': date_label,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [camera_image_folder_id]
        }

        file = drive.files().create(body=file_metadata,
                                    supportsAllDrives=True).execute()

        date_folder_id = file.get('id')

    picture_info = drive.files().list(
        corpora="drive",
        driveId=google_drive_folder_id,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q="'" + date_folder_id + "'" + " in parents and trashed = false and name='" + picture_label + "'"
    ).execute().get('files', [])

    if len(picture_info) > 0:
        print("Picture already exists! Not overwriting")

    # If there is NOT a picture by that name, write one
    if len(picture_info) == 0:
        file_metadata = {
            'name': [picture_label],
            'parents': [date_folder_id]
        }
        media = MediaFileUpload(original_pic_path,
                                mimetype='image/jpg',
                                resumable=True)

        file = drive.files().create(body=file_metadata,
                                    media_body=media,
                                    supportsAllDrives=True).execute()

    db_functions.write_photo_info(
        db=db,
        drive_filename=picture_label,
        camera_ID=camera_ID,
        SourceFile="none",
        FileName="none",
        FileSize=os.path.getsize(original_pic_path),
        DateTimeOriginal=datetime_string,
        original_tz=timezone,
        DateTimeOriginalUTC=datetime_original_arrow.datetime,
        high_water=False
    )

    blurring_functions.blur_image(camera_ID.replace("CAM_", ""), reduced_image_path)
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

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    some_photo_info = db_functions.get_latest_photo_info(db=db, camera_ID=camera_ID)

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

    camera_info = db_functions.add_camera(db=db, place=place, camera_ID=camera_ID, lng=lng, lat=lat, camera_label=camera_label, sensor_ID=sensor_ID)

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

    if not (correct_username and correct_password):
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