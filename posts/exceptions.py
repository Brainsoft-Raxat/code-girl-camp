from fastapi import HTTPException

class PostNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Post Not Found")
