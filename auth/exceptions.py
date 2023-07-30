from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User Not Found")


class UserExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Username exists")
