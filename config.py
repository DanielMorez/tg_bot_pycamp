from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Основные настройки бота
    BOT_TOKEN: str
    REDIS_URL: str
    
    # API настройки
    API_BASE_URL: str
    API_LOGIN: str
    API_PASSWORD: str
    
    # Настройки кеширования
    PHONE_CACHE_TTL: int = 7 * 24 * 60 * 60  # 7 дней в секундах
    AUTH_LINK_CACHE_TTL: int = 600  # 10 минут в секундах
    
    # Настройки UI
    SUPPORT_BOT_URL: str = "https://t.me/your_support_bot"
    CHANNEL_URL: str = "https://t.me/codelis_digest"
    LOADING_STICKER_ID: str = "CAACAgIAAxkBAAExqU9nq5ox8OKuKAR3gVTbqlxsOocsYAACeBsAArZjKElJPqq2J-v4QTYE"
    
    # Сообщения об ошибках
    API_ERROR_MESSAGE: str = (
        "Наш сервис сейчас немного прилёг отдохнуть — мы быстро чиним и перезагружаем,"
        " чтобы всё снова работало как часы👾"
    )
    LOADING_MESSAGE: str = "Генерируем ссылку..."

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
