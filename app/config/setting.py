import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # REDIS
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str = None
    REDIS_PASSWORD: str = None

    # GITHUB
    GITHUB_BASE_URL: str = 'https://api.github.com'
    GITHUB_TOKEN: str = None
    GITHUB_PAGE_SIZE: int = 100
    GITHUB_REPO_URL_SAVE_FILES: str = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


dotenv.load_dotenv()
setting = Settings()
