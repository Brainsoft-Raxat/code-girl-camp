from fastapi import FastAPI
from config import settings
from routers.posts import router as posts_router
from database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def hello_world():
    return settings.dict()


app.include_router(router=posts_router, prefix="/posts", tags=["Posts"])
