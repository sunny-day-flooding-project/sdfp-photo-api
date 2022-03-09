# from typing import List, Optional
import datetime

from pydantic import BaseModel


class photo_info_model_base(BaseModel):
    drive_filename = str
    camera_ID = str
    # SourceFile = str
    # FileName = str
    # FileSize = float
    # DateTimeOriginal = str
    # original_tz = str
    # DateTimeOriginalUTC = datetime.datetime
    # high_water = bool


class photo_info(photo_info_model_base):
    high_water = bool

    class Config:
        orm_mode = True
