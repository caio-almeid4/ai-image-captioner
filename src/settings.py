from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str = 'sa-east-1'
    BUCKET_NAME: str = 'ai-image-captioner'

    ALLOWED_EXTENSIONS: Set = {'jpg', 'jpeg', 'png'}

    DATABASE_URL: str

    OPENAI_API_KEY: str
    DEFAULT_TOP_P: float = 1
    DEFAULT_TEMPERATURE: float = 0.5
