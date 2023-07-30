from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str
    content: str
    author: str
    country: str
    location: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    author: str | None = None
    country: str | None = None
    location: str | None = None
