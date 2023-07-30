
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    avatar: str


class UserUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    surname: str | None = None
    avatar: str
