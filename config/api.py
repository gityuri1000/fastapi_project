from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    BASE_URL: str
    TOKEN: str

    model_config = SettingsConfigDict(
        env_file="api.env",
        env_file_encoding="utf-8",
        extra="allow"
    )

api_settings = Settings()