import json
import logging
from typing import Optional
import redis.asyncio as redis
from config import settings
from src.constants import CACHE_PHONE_PREFIX, CACHE_AUTH_LINK_PREFIX

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL, decode_responses=True
            )
            self.phone_cache_ttl = settings.PHONE_CACHE_TTL
            self.auth_link_cache_ttl = settings.AUTH_LINK_CACHE_TTL
            self._redis_available = True
        except Exception as e:
            logger.error(f"Не удалось подключиться к Redis: {e}")
            self._redis_available = False

    async def set_phone(self, user_id: int, phone: str) -> None:
        """Сохраняет номер телефона в кеше на 7 дней"""
        if not self._redis_available:
            logger.warning("Redis недоступен, пропускаем сохранение номера телефона")
            return

        try:
            key = f"{CACHE_PHONE_PREFIX}{user_id}"
            await self.redis_client.setex(key, self.phone_cache_ttl, phone)
            logger.info(f"Номер телефона сохранен в кеше для пользователя {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении номера телефона в кеше: {e}")

    async def get_phone(self, user_id: int) -> Optional[str]:
        """Получает номер телефона из кеша"""
        if not self._redis_available:
            logger.warning("Redis недоступен, пропускаем получение номера телефона")
            return None

        try:
            key = f"{CACHE_PHONE_PREFIX}{user_id}"
            phone = await self.redis_client.get(key)
            if phone:
                logger.info(f"Номер телефона найден в кеше для пользователя {user_id}")
            return phone
        except Exception as e:
            logger.error(f"Ошибка при получении номера телефона из кеша: {e}")
            return None

    async def set_auth_link(
        self, user_id: int, auth_link: str, expires_at: int
    ) -> None:
        """Сохраняет ссылку авторизации в кеше"""
        if not self._redis_available:
            logger.warning("Redis недоступен, пропускаем сохранение ссылки авторизации")
            return

        try:
            key = f"{CACHE_AUTH_LINK_PREFIX}{user_id}"
            # Сохраняем ссылку и время истечения как JSON
            data = {"link": auth_link, "expires_at": expires_at}
            await self.redis_client.setex(
                key, self.auth_link_cache_ttl, json.dumps(data)
            )
            logger.info(
                f"Ссылка авторизации сохранена в кеше для пользователя {user_id}"
            )
        except Exception as e:
            logger.error(f"Ошибка при сохранении ссылки авторизации в кеше: {e}")

    async def get_auth_link(self, user_id: int) -> Optional[dict]:
        """Получает ссылку авторизации из кеша"""
        if not self._redis_available:
            logger.warning("Redis недоступен, пропускаем получение ссылки авторизации")
            return None

        try:
            key = f"{CACHE_AUTH_LINK_PREFIX}{user_id}"
            data = await self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Ошибка при получении ссылки авторизации из кеша: {e}")
            return None

    async def delete_phone(self, user_id: int) -> None:
        """Удаляет номер телефона из кеша"""
        if not self._redis_available:
            logger.warning("Redis недоступен, пропускаем удаление номера телефона")
            return

        try:
            key = f"{CACHE_PHONE_PREFIX}{user_id}"
            await self.redis_client.delete(key)
            logger.info(f"Номер телефона удален из кеша для пользователя {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при удалении номера телефона из кеша: {e}")

    async def close(self):
        """Закрывает соединение с Redis"""
        if self._redis_available:
            try:
                await self.redis_client.close()
                logger.info("Соединение с Redis закрыто")
            except Exception as e:
                logger.error(f"Ошибка при закрытии соединения с Redis: {e}")


# Создаем глобальный экземпляр сервиса кеша
cache_service = CacheService()
