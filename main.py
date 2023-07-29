from fastapi import FastAPI
from pydantic import BaseModel

posts = {
    0: {
        "title": "blah blah",
        "content": "content",
        "author": "haha"
    }
}
last_id = 0

class PostCreate(BaseModel):
    title: str
    content: str
    author: str


app = FastAPI()


@app.get("/posts")
def get_all_posts():
    return list(posts.values())

@app.post("/posts")
def create_post(post_data: PostCreate):
    global last_id
    new_id = last_id + 1 
    posts[new_id] = post_data.dict()
    last_id = new_id
    return new_id
