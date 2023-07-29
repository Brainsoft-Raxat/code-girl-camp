from main import app
from users.schemas import UserCreate, UserUpdate
from users.exceptions import UserNotFound

users = {

}

last_user_id = -1


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
