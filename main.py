from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from posts.schemas import PostCreate, PostUpdate
from users.schemas import UserCreate, UserUpdate


app = FastAPI()

import posts.router
import users.router
