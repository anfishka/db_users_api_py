from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, get_db
#from crud import create_note, get_notes, get_note_by_id, update_note, delete_note
from scemas import UserScema
from models import Base, User

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/user/{user_name}")
async def get_users(user_name, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.name == user_name).first()
    return users

@app.post("/adduser")
async def adduser(request:UserScema, db: Session = Depends(get_db)):
    user = User(name=request.name, email= request.email, nickname=request.nickname)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.put("/user/{user_id}")
async def update_user(user_id: int, request: UserScema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = request.name
    user.email = request.email
    user.nickname = request.nickname
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": user}


@app.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}