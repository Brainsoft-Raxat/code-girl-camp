# pip install "passlib[bcrypt]"
# pip install python-jose

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "6dc7326daea2e372a5aee9fcd14871af7aea4b2a8ce3f1e52fa7eac6e71b3f4f"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expire_date: datetime):
    to_encode = data.copy()
    to_encode.update({"exp": expire_date})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
