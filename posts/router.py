from fastapi import APIRouter
from posts.schemas import PostCreate, PostUpdate
from posts.exceptions import PostNotFound
from posts import service

router = APIRouter()


@router.get("/")
async def get_all_posts():
    posts = await service.get_all_posts()

    return posts


@router.post("/")
async def create_post(post_data: PostCreate):
    post = await service.create_post(post_data)

    return {"id": post.id}


@router.get("/{post_id}")
async def get_post(post_id: int):
    post = await service.get_post_by_id(post_id)

    if not post:
        raise PostNotFound()

    return post


@router.put("/{post_id}")
async def update_post(post_id: int, post_data: PostUpdate):
    post = await service.get_post_by_id(post_id)

    if not post:
        raise PostNotFound()

    post = await service.update_post(post_id, post_data)

    return post


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    post = await service.get_post_by_id(post_id)

    if not post:
        raise PostNotFound()

    await service.delete_post(post_id)

    return post_id
