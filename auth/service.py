from sqlalchemy import select, insert, update, delete
from auth.schemas import UserCreate, UserUpdate
from auth.exceptions import UserNotFound, UserExists
from auth.security import hash_password
from database import database, users


async def get_user_by_username(username: str):
    select_query = select(users).where(users.c.username == username)

    user = await database.fetch_one(select_query)
    if not user:
        raise UserNotFound

    return user


async def create_user(user_data: UserCreate):
    try:
        user = await get_user_by_username(user_data.username)
    except UserNotFound:
        pass

    if user:
        raise UserExists()

    user_data.password = hash_password(user_data.password)
    insert_query = insert(users).values(
        user_data.model_dump()).returning(users.c.id)

    return await database.fetch_one(insert_query)


async def get_all_users(skip: int = 0, limit: int = 100):
    select_query = select(
        users.c.id,
        users.c.username,
        users.c.name,
        users.c.surname,
        users.c.avatar
    ).offset(skip).limit(limit)

    return await database.fetch_all(select_query)


async def get_user_by_id(user_id: int):
    select_query = select(
        users.c.id,
        users.c.username,
        users.c.name,
        users.c.surname,
        users.c.avatar
    ).where(users.c.id == user_id)

    user = await database.fetch_one(select_query)
    if not user:
        raise UserNotFound()

    return user


async def update_user_by_id(user_id: int, user_data: UserUpdate):
    user = await get_user_by_id(user_id)

    try:
        foreign_user = await get_user_by_username(user_data.username)
    except UserNotFound:
        pass

    if foreign_user and foreign_user.username != user.username:
        raise UserExists()

    update_query = (
        update(users)
        .values(user_data.model_dump(exclude_unset=True))
        .where(users.c.id == user_id)
        .returning(
            users.c.id,
            users.c.username,
            users.c.name,
            users.c.surname,
            users.c.avatar))

    return await database.fetch_one(update_query)


async def delete_user_by_id(user_id: int):
    await get_user_by_id(user_id)

    delete_query = delete(users).where(users.c.id == user_id)

    return await database.execute(delete_query)
