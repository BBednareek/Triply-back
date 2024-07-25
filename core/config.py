import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DB_USER: str = os.getenv("MYSQL_USER")
    DB_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    DB_NAME: str = os.getenv("MYSQL_DATABASE")
    DB_HOST: str = os.getenv("MYSQL_HOST")
    DB_PORT: str = os.getenv("MYSQL_PORT")

    @property
    def database_url(self) -> str:
        return (f"mysql+pymysql://{self.DB_USER}"
                f":%s@{self.DB_HOST}"
                f":{self.DB_PORT}/{self.DB_NAME}"
                % quote_plus(self.DB_PASSWORD)
                )

#TODO jwt_secret

    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("JWT_TOKEN_EXPIRE_MINUTES", 60)


def get_settings() -> Settings:
    return Settings()
