from pydantic import BaseModel

class FileMetadataBase(BaseModel):
    filename: str
    folder: str
    url: str

class FileMetadataCreate(FileMetadataBase):
    pass

class FileMetadata(FileMetadataBase):
    id: int

    class Config:
        orm_mode = True
