from databases import Database
from config import settings
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Identity,
    DateTime,
    create_engine,
    func
)

DATABASE_URL = settings.DATABASE_URL

database = Database(DATABASE_URL, force_rollback=settings.IS_TESTING)
metadata = MetaData()

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("title", String, nullable=False),
    Column("content", String, nullable=False),
    Column("author", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now())
)

engine = create_engine(DATABASE_URL)

metadata.create_all(engine)


