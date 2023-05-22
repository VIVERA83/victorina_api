import os

from pydantic import BaseModel, BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class Postgres(BaseModel):
    db: str
    user: str
    password: str
    host: str
    port: int
    db_schema: str = "public"

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Log(BaseModel):
    level: str = "INFO"
    guru: bool = False
    traceback: bool = False


class Settings(BaseSettings):
    postgres: Postgres
    logging: Log
    host: str
    port: int

    class Config:
        env_nested_delimiter = "__"
        env_file = BASE_DIR + "/.env"
        enf_file_encoding = "utf-8"
