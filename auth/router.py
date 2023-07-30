from fastapi import APIRouter, Depends
from auth.schemas import UserCreate, UserUpdate
from auth import service

router = APIRouter()


@router.get("/users")
async def get_all_users(skip: int = 0, limit: int = 100):
    return await service.get_all_users(skip, limit)


@router.post("/users")
async def create_user(user_data: UserCreate):
    return await service.create_user(user_data)


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return await service.get_user_by_id(user_id)


@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate):
    return await service.update_user_by_id(user_id, user_data)


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    await service.delete_user_by_id(user_id)
    return user_id
