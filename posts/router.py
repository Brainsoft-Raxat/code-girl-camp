from main import app
from posts.schemas import PostCreate, PostUpdate
from posts.exceptions import PostNotFound

posts = {
    0: {
        "title": "blah blah",
        "content": "content",
        "author": "haha"
    }
}

last_post_id = 0

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