from sqlalchemy import Column, Integer, String
from .database import Base

class FileMetadata(Base):
    __tablename__ = 'filemetadata'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    folder = Column(String, index=True)
    url = Column(String)
