import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # REDIS
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str = None
    REDIS_PASSWORD: str = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


dotenv.load_dotenv()
setting = Settings()
