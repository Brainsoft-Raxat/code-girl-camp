from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    IS_TESTING: bool = False


settings = Config()
