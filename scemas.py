from pydantic import BaseModel, field_validator
from typing import Optional

from sqlalchemy.util.queue import Empty


class UserCreateSchema(BaseModel):
    name: str
    email: str
    nickname: str

    # Валидация всех полей
    @field_validator("name", "email", "nickname")
    def check_not_string(cls, value):
        if value.lower() == "string" or value == Empty:
            raise ValueError("Field value cannot be 'this value'")
        return value


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: str
    nickname: str

    class Config:
        orm_mode = True