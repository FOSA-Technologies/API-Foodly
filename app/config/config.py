
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    db_url:str = "postgresql://postgres:root@localhost:5432/foodly"
    database: str = "postgresql"
    db_name: str = "foodly"
    db_user: str = "postgres"
    db_host: str = "localhost"
    api_url: str = "http://localhost:8000"
    db_password: str = "root"
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()