from pydantic import BaseModel

class UserScema(BaseModel):
    name: str
    email: str
    nickname: str