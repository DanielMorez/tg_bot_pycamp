from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS_URL: str
    API_BASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
