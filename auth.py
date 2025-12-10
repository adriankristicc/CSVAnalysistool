# auth.py
import hashlib
from models import User
from database import get_db
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username: str, password: str, db: Session):
    # Provjera da li postoji
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Kreiraj korisnika
    new_user = User(
        username=username,
        hashed_password=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    return {"message": "User registered"}