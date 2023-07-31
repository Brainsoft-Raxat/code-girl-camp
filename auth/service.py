from sqlalchemy import select, insert, update, delete
from auth.schemas import UserCreate, UserUpdate, UserAuth, TokenResponse
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from auth.exceptions import UserNotFound, UserExists, InvalidAuthCredentials, InvalidSession
from exceptions import InternalServerError
from auth.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import database, users, sessions
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/token")


async def create_session(user_id: int, token: str, expire_date: datetime):
    insert_query = insert(sessions).values(
        user_id=user_id, token=token, expire_date=expire_date).returning(sessions.c.id)
    return await database.fetch_one(insert_query)


async def get_session_by_token(token: str):
    select_query = select(sessions).where(sessions.c.token == token)
    return await database.fetch_one(select_query)


async def delete_session(token: str):
    delete_query = delete(sessions).where(sessions.c.token == token)
    return await database.execute(delete_query)


async def login_for_access_token(auth_data: UserAuth):
    try:
        user = await get_user_by_username(auth_data.username)
    except UserNotFound:
        raise InvalidAuthCredentials()

    if not verify_password(auth_data.password, user["password"]):
        raise InvalidAuthCredentials()

    access_token_expire_date = datetime.utcnow(
    ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expire_date=access_token_expire_date)

    session = await create_session(user["id"], access_token, expire_date=access_token_expire_date)

    if not session:
        raise InternalServerError()

    return TokenResponse(access_token=access_token)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    session = await get_session_by_token(token)
    if not session or (session and session["expire_date"] < datetime.utcnow()):
        raise InvalidSession()
    return session["user_id"]


async def get_user_by_username(username: str):
    select_query = select(users).where(users.c.username == username)

    user = await database.fetch_one(select_query)
    if not user:
        raise UserNotFound

    return user


async def create_user(user_data: UserCreate):
    user = None

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
