from databases import Database
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    Identity,
    DateTime,
    ForeignKey,
    func,
    create_engine,
)

# pip install databases sqlalchemy asyncpg psycopg2-binary
# driver://<POSTGRES_USER>:<PASSWORD>@<HOSTNAME>:<PORT>/<DATABASE_NAME>
DATABASE_URL = "postgresql://roland:password@localhost:5432/postgres"

database = Database(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column("name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("avatar", String)
)

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("title", String, nullable=False),
    Column("content", Text, nullable=False),
    Column("author", ForeignKey("users.id"), nullable=False),
    Column("country", String, nullable=False),
    Column("location", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)

sessions = Table(
    "sessions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("token", String, unique=True, index=True, nullable=False),
    Column("expire_date", DateTime, nullable=False)
)


engine = create_engine(DATABASE_URL)

metadata.create_all(engine)
