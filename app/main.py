from fastapi import FastAPI, Depends, HTTPException
from fastai import *
from fastai.vision import *
from sqlalchemy.orm import Session

from . import models
from .collab import *
from .utils import *
from .db import SessionLocal, engine

app = FastAPI()

external_dataset_path = download_ml20m()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    # Most popular movies
    return {"Hello": "World"}

@app.get("/user/{user_id}")
def send_recommendations(user_id: int, q: str = None):
    return {"item_id": user_id, "q": q}

@app.get("/background_process/generate_recommendations")
def generate_recommendations(external_dataset_path: Path= external_dataset_path, db: Session = Depends(get_db)):
    ratings = models.get_ratings(db)
    status_message = get_recommendations(ratings, external_dataset_path)
    return {"message": status_message}