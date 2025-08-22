import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    SECRET_KEY: str = "default_secret_key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = "3306"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password123"
    MYSQL_DB: str = "fastapi_assignment"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MEDIA_DIR: str = os.path.join(BASE_DIR, "media")

config = Config()
