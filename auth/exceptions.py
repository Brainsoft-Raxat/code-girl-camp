from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User Not Found")


class UserExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Username exists")


class InvalidAuthCredentials(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Invalid username or password")


class InvalidSession(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Invalid session")
