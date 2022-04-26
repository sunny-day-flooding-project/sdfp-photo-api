import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import models


def get_latest_photo_info(db: Session, camera_ID: str):
    return db.query(models.photo_info_model).filter(models.photo_info_model.camera_ID == camera_ID).order_by(
        desc('DateTimeOriginalUTC')).first()


def get_photo_info(db: Session, drive_filename: str):
    return db.query(models.photo_info_model).filter(models.photo_info_model.drive_filename == drive_filename).first()


def add_camera(db: Session,
               place: str,
               camera_ID: str,
               lng: float,
               lat: float
                     ):
    camera_in_db = db.query(models.camera_locations_model).filter(models.camera_locations_model.camera_ID == camera_ID).all()

    camera_exists = len(camera_in_db) > 0

    if(camera_exists == True):
        return "Camera already exists!"

    if(camera_exists == False):

        new_camera = models.camera_locations_model(
            place=place,
            camera_ID=camera_ID,
            lng=lng,
            lat=lat
        )

        db.add(new_camera)
        db.commit()
        db.refresh(new_camera)

        return "SUCCESS! New camera added"

def write_photo_info(db: Session,
                     drive_filename: str,
                     camera_ID: str,
                     SourceFile: str,
                     FileName: str,
                     FileSize: float,
                     DateTimeOriginal: str,
                     original_tz: str,
                     DateTimeOriginalUTC: str,
                     high_water: bool
                     ):
    photo_in_db = db.query(models.photo_info_model).filter(models.photo_info_model.drive_filename == drive_filename).all()

    photo_exists = len(photo_in_db) > 0

    if(photo_exists == True):
        return "Photo already within database"

    if(photo_exists == False):

        new_photo_data = models.photo_info_model(
            drive_filename=drive_filename,
            camera_ID=camera_ID,
            SourceFile=SourceFile,
            FileName=FileName,
            FileSize=FileSize,
            DateTimeOriginal=DateTimeOriginal,
            original_tz=original_tz,
            DateTimeOriginalUTC=DateTimeOriginalUTC,
            high_water=high_water
        )

        db.add(new_photo_data)
        db.commit()
        db.refresh(new_photo_data)

        return
