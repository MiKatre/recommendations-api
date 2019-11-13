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
    # Nothing for now
    return {"Hello": "World"}

# Create up to date dataset and send to colab
@app.get("/background/update/model")
def generate_dataset(external_dataset_path: Path= external_dataset_path, db: Session = Depends(get_db)):
    ratings = models.get_ratings(db)
    status_message = create_dataset(ratings, external_dataset_path)
    return {"message": 'Dataset uploaded'}

# Fetch recommendations and insert into db
@app.get("/background/update/recommendations")
def insert_recommendations(external_dataset_path: Path= external_dataset_path, db: Session = Depends(get_db)):
    recommendations = get_available_predictions()
    result = models.insert_recommendations(db, recommendations)
    return {"message": result}


# Automatically does everything above. 
# Needs powerful server to work
@app.get("/background/retrain")
def fully_update_recommendations(external_dataset_path: Path= external_dataset_path, db: Session = Depends(get_db)):
    ratings = models.get_ratings(db)
    recommendations = fully_retrain_model_and_update_recommendations(ratings, external_dataset_path)
    result = models.insert_recommendations(db, recommendations)
    return {"message": "Recommendations updated"}