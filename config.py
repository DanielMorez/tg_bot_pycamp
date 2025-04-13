from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    REDIS_URL: str
    API_BASE_URL: str
    API_LOGIN: str
    API_PASSWORD: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
