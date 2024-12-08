from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import (
    get_all_users,
    get_user_by_name,
    create_user,
    update_user,
    delete_user,
    update_user_partially
)
from scemas import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from models import User

app = FastAPI()

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@app.get("/user/{user_name}")
async def get_user(user_name: str, db: Session = Depends(get_db)):
    return get_user_by_name(db, user_name)

@app.post("/adduser")
async def add_user(request: UserCreateSchema, db: Session = Depends(get_db)):
    return create_user(db, request.name, request.email, request.nickname)

@app.put("/user/{user_id}")
async def update_user_route(user_id: int, request: UserCreateSchema, db: Session = Depends(get_db)):
    return update_user(db, user_id, request.name, request.email, request.nickname)

# @app.patch("/user/{user_id}", response_model=UserResponseSchema)
# async def patch_user(user_id: int, request: UserUpdateSchema, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail=f"User with id '{user_id}' is absent in db!"
#         )
#
#     request_update = request.dict(exclude_unset=True)
#     for key, value in request_update.items():
#         if value is None or value == "" or value.lower() == "string":
#             continue
#         if hasattr(user, key):
#             setattr(user, key, value)
#
#     db.commit()
#     db.refresh(user)
#
#     return user

@app.patch("/user/{user_id}", response_model=UserResponseSchema)
async def patch_user(user_id: int, request: UserUpdateSchema, db: Session = Depends(get_db)):
    # Преобразуем данные запроса
    updates = request.dict(exclude_unset=True)

    # Вызываем функцию из crud.py
    user = update_user_partially(db, user_id, updates)

    # Возвращаем обновлённого пользователя
    return user

@app.delete("/user/{user_id}")
async def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)