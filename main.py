from fastapi import FastAPI
from database import init_db

app = FastAPI(title="CSV Analysis Tool")

init_db()

from fastapi import FastAPI, Depends
from database import init_db, get_db
from auth import register
from sqlalchemy.orm import Session

app = FastAPI()

init_db()

@app.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    return register(username, password, db)