from fastapi import APIRouter, Form, HTTPException
import os
from app.main import UPLOAD_FOLDER

router = APIRouter()

@router.post("/create_folder/")
def create_folder(folder: str = Form(...)):
    folder_path = os.path.join(UPLOAD_FOLDER, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return {"message": "Folder created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Folder already exists")
