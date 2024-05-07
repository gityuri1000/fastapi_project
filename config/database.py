from typing import Any, Optional
from pydantic import field_validator, PostgresDsn, Field, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


def validation_decorator():
    def wrapper(value: Any, info: ValidationInfo):
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_NAME"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_HOST"),
            port=info.data.get("POSTGRES_PORT"),
            path=info.data.get("POSTGRES_DB")
        )
    
    return wrapper

class Settings(BaseSettings):

    POSTGRES_NAME: str
    POSTGRES_PASSWORD: str = Field(min_length=3)
    POSTGRES_HOST: str = Field(default="localhost", validate_default=True)
    POSTGRES_PORT: int
    POSTGRES_DB: str

    DATABASE_URI: Optional[PostgresDsn] = None

    uri_validation = field_validator("DATABASE_URI", mode="before")(validation_decorator())

    model_config = SettingsConfigDict(
        # env_file=env_path,
        env_file="database.env",
        env_file_encoding="utf-8"
    )

settings = Settings()