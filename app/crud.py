from sqlalchemy.orm import Session
from . import models, schemas

def create_file_metadata(db: Session, file_metadata: schemas.FileMetadataCreate):
    db_file_metadata = models.FileMetadata(**file_metadata.dict())
    db.add(db_file_metadata)
    db.commit()
    db.refresh(db_file_metadata)
    return db_file_metadata

def get_files(db: Session, folder: str = None):
    if folder:
        return db.query(models.FileMetadata).filter(models.FileMetadata.folder == folder).all()
    return db.query(models.FileMetadata).all()

def delete_file_metadata(db: Session, filename: str, folder: str = None):
    query = db.query(models.FileMetadata).filter(models.FileMetadata.filename == filename)
    if folder:
        query = query.filter(models.FileMetadata.folder == folder)
    query.delete()
    db.commit()
