from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import folder, image
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_FOLDER = '/home/bucket/ONDC'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.include_router(folder.router, prefix="/api")
app.include_router(image.router, prefix="/api")
