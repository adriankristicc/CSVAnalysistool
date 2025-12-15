from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import init_db, get_db
from auth import register
from analysis import analyze_csv

app = FastAPI(title="CSV Analysis Tool")

init_db()

@app.get("/")
def home():
    return {"message": "App radi"}

@app.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    return register(username, password, db)

@app.get("/analyze")
def analyze(file_path: str):

    return analyze_csv(file_path)

from fastapi import UploadFile, File
import os
import shutil
from analysis import analyze_csv

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.post("/upload-csv")
def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        return {"error": "Uploaduj .csv fajl"}

    save_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return analyze_csv(save_path)