
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    name: str
    surname: str


class UserUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    surname: str | None = None