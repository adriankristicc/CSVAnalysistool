import os
import shutil

from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from database import init_db, get_db
from auth import register, login
from analysis import analyze_csv
from schemas import CSVAnalysisResponse

app = FastAPI(title="CSV Analysis Tool")

# kreiraj bazu/tabele pri startu
init_db()

# folder za upload
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"status": "API radi"}


# -------- AUTH (BE) --------
@app.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    return register(username, password, db)


@app.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    return login(username, password, db)


# -------- CSV ANALYZE --------
@app.get("/analyze")
def analyze(file_path: str):
    return analyze_csv(file_path)


# -------- CSV UPLOAD + ANALYZE --------
@app.post("/upload-csv", response_model=CSVAnalysisResponse)
def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Dozvoljeni su samo CSV fajlovi")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return analyze_csv(file_path)