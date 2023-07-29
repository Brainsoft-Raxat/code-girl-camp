from sqlalchemy import insert, select
from databases.interfaces import Record
from datetime import datetime

from schemas import PostCreate
from database import posts, database


async def create_post(post: PostCreate) -> Record | None:
    insert_query = (
        insert(posts)
        .values(
            {
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "created_at": datetime.utcnow(),
            }
        ).returning(posts)
    )

    return await database.fetch_one(insert_query)

async def get_all_posts():
    select_query = select([posts])
    return await database.fetch_all(select_query)
