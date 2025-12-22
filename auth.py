import hashlib
import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User, Token


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=username, hashed_password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered", "id": new_user.id, "username": new_user.username}


def login(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.hashed_password != hash_password(password):
        raise HTTPException(status_code=401, detail="Wrong username or password")

    tok = secrets.token_urlsafe(32)
    db.add(Token(token=tok, user_id=user.id))
    db.commit()

    return {"message": "Logged in", "token": tok, "username": user.username}