from fastapi import APIRouter, Depends
from posts.schemas import PostCreate, PostUpdate
from posts import service
from auth.service import get_current_user

router = APIRouter()


@router.get("")
async def get_all_posts():
    return await service.get_all_posts()


@router.post("")
async def create_post(post_data: PostCreate, user_id=Depends(get_current_user)):
    post_data.author = user_id

    return await service.create_post(post_data)


@router.get("/{post_id}")
async def get_post(post_id: int):
    return await service.get_post_by_id(post_id)


@router.put("/{post_id}")
async def update_post(post_id: int, post_data: PostUpdate, user_id=Depends(get_current_user)):
    post_data.author = user_id
    return await service.update_post(post_id, post_data)


@router.delete("/{post_id}")
async def delete_post(post_id: int, user_id=Depends(get_current_user)):
    await service.delete_post(post_id)
    return {"id": post_id}
