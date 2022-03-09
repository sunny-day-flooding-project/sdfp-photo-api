from sqlalchemy import Boolean, Column, String, Float, DateTime

from database import Base


class photo_info_model(Base):
    __tablename__ = "photo_info"

    drive_filename = Column(String, primary_key=True, index=True)
    camera_ID = Column(String, index=True)
    SourceFile = Column(String, index=True)
    FileName = Column(String, index=True)
    FileSize = Column(Float, index=True)
    DateTimeOriginal = Column(String, index=True)
    original_tz = Column(String, index=True)
    DateTimeOriginalUTC = Column(DateTime, index=True)
    high_water = Column(Boolean, index=True)


