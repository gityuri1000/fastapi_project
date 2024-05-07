from pydantic import BaseModel

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file="jwt.env",
        env_file_encoding="utf-8",
        extra="allow"
    )

jwt_settings = Settings()