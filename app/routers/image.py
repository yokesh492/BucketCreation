from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import os
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, models, schemas, utils
# from app.main import UPLOAD_FOLDER

router = APIRouter()
UPLOAD_FOLDER = '/home/bucket/ONDC'

@router.post("/upload_image/", response_model=schemas.FileMetadata)
async def upload_image(file: UploadFile = File(...), folder: str = Form(""), db: Session = Depends(get_db)):
    folder_path = os.path.join(UPLOAD_FOLDER, folder) if folder else UPLOAD_FOLDER
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    filename = file.filename
    file_path = os.path.join(folder_path, filename)
    compressed_image = utils.compress_image(file)
    
    with open(file_path, 'wb') as f:
        f.write(compressed_image.getvalue())
    
    file_url = f"https://bucket.vizdale.com/{folder}/{filename}" if folder else f"https://bucket.vizdale.com/{filename}"
    
    file_metadata = schemas.FileMetadataCreate(filename=filename, folder=folder, url=file_url)
    return crud.create_file_metadata(db=db, file_metadata=file_metadata)

@router.delete("/delete_image/")
def delete_image(filename: str, folder: str = "", db: Session = Depends(get_db)):
    folder_path = os.path.join(UPLOAD_FOLDER, folder) if folder else UPLOAD_FOLDER
    file_path = os.path.join(folder_path, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        crud.delete_file_metadata(db=db, filename=filename, folder=folder)
        return {"message": "File deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="File not found")

@router.get("/download_image/")
def download_image(filename: str, folder: str = ""):
    folder_path = os.path.join(UPLOAD_FOLDER, folder) if folder else UPLOAD_FOLDER
    file_path = os.path.join(folder_path, filename)
    
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@router.get("/list_images/", response_model=list[schemas.FileMetadata])
def list_images(folder: str = "", db: Session = Depends(get_db)):
    files = crud.get_files(db=db, folder=folder)
    return files
