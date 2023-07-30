from posts.schemas import PostCreate, PostUpdate
from posts.exceptions import PostNotFound
from database import posts, database
from sqlalchemy import insert, select, update, delete
from datetime import datetime


async def create_post(post_data: PostCreate):
    # insert_query = "INSERT INTO posts (title, content, author, country, location, created_at) VALUES"
    insert_query = insert(posts).values(
        post_data.model_dump()
    ).returning(posts.c.id)

    return await database.fetch_one(insert_query)


async def get_all_posts(skip: int = 0, limit: int = 100):

    select_query = select(posts).offset(skip).limit(limit)

    return await database.fetch_all(select_query)


async def get_post_by_id(post_id: int):
    select_query = select(posts).where(posts.c.id == post_id)

    post = await database.fetch_one(select_query)

    if not post:
        raise PostNotFound()

    return post


async def update_post(post_id: int, post_data: PostUpdate):
    await get_post_by_id(post_id)
    
    update_query = (update(posts)
                    .values(post_data.model_dump(exclude_unset=True))
                    .where(posts.c.id == post_id)).returning(posts)

    return await database.fetch_one(update_query)


async def delete_post(post_id: int):
    await get_post_by_id(post_id)

    delete_query = delete(posts).where(posts.c.id == post_id)

    return await database.execute(delete_query)
