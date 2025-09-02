import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from config import settings
from src.handlers import register_handlers
from src.services.cache import cache_service

# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN)
storage = RedisStorage.from_url(settings.REDIS_URL)
dp = Dispatcher(storage=storage)

# Регистрация обработчиков
register_handlers(dp)


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        # Закрываем соединение с Redis при завершении работы бота
        await cache_service.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
