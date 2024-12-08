from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from fastapi import HTTPException

from scemas import UserUpdateSchema


def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_name(db: Session, user_name: str):
    return db.query(User).filter(User.name == user_name).first()

def create_user(db: Session, name: str, email: str, nickname: str):
    user = User(name=name, email=email, nickname=nickname)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, name: str, email: str, nickname: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.email = email
    user.nickname = nickname
    db.commit()
    db.refresh(user)
    return user

def update_user_partially(db: Session, user_id: int, updates: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    for key, value in updates.items():
        if value and value.lower() == "string":
            continue
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
