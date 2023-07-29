from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

posts = {
    0: {
        "title": "blah blah",
        "content": "content",
        "author": "haha"
    }
}

last_post_id = 0

users = {

}

last_user_id = -1


class PostNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Post Not Found")

class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User Not Found")


class PostCreate(BaseModel):
    title: str
    content: str
    author: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    author: str | None = None


class UserCreate(BaseModel):
    username: str
    name: str
    surname: str


class UserUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    surname: str | None = None


app = FastAPI()


@app.get("/posts")
def get_all_posts():
    return list(posts.values())


@app.post("/posts")
def create_post(post_data: PostCreate):
    global last_post_id
    new_id = last_post_id + 1
    posts[new_id] = post_data.dict()
    last_post_id = new_id
    return new_id


@app.get("/post/{post_id}")
def get_post(post_id: int):
    if post_id not in posts:
        raise PostNotFound()
    return posts[post_id]


@app.put("/post/{post_id}")
def update_post(post_id: int, post_data: PostUpdate):
    if post_id not in posts:
        raise PostNotFound()

    post_dict = post_data.dict(exclude_unset=True)
    posts[post_id].update(post_dict)

    return posts[post_id]


@app.delete("/post/{post_id}")
def delete_post(post_id: int):
    if post_id not in posts:
        raise PostNotFound()
    del posts[post_id]

    return post_id


@app.get("/users")
def get_all_users():
    return list(users.values())

@app.post("/users")
def create_user(user_data: UserCreate):
    global last_user_id
    new_id = last_user_id + 1
    users[new_id] = user_data.dict()
    last_user_id = new_id
    return new_id


@app.get("/user/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise UserNotFound()
    return users[user_id]


@app.put("/user/{user_id}")
def update_user(user_id: int, user_data: UserUpdate):
    if user_id not in users:
        raise UserNotFound()

    user_dict = users.dict(exclude_unset=True)
    users[user_id].update(user_dict)

    return users[user_id]


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise UserNotFound()
    del users[user_id]

    return user_id
