from fastapi import APIRouter
from schemas import PostCreate
import service



router = APIRouter()

@router.get("/")
async def read_all_posts():
    posts = await service.get_all_posts()
    return posts

@router.post("/")
async def create_post(post_data: PostCreate):
    post = await service.create_post(post=post_data)
    return {
        "id": post["id"],
        "title": post["title"]
    }