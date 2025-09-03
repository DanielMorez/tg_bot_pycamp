import time
from typing import Optional

from aiohttp import ClientConnectorError, ContentTypeError

from config import settings
from src.exceptions import AuthError
from src.services.auth import user_login
from src.services.cache import cache_service


class AuthService:
    """Сервис для работы с авторизацией пользователей"""

    @staticmethod
    async def get_cached_auth_link(user_id: int) -> Optional[dict]:
        """Получает кешированную ссылку авторизации"""
        return await cache_service.get_auth_link(user_id)

    @staticmethod
    async def get_cached_phone(user_id: int) -> Optional[str]:
        """Получает кешированный номер телефона"""
        return await cache_service.get_phone(user_id)

    @staticmethod
    async def save_phone_to_cache(user_id: int, phone: str) -> None:
        """Сохраняет номер телефона в кеш"""
        await cache_service.set_phone(user_id, phone)

    @staticmethod
    async def save_auth_link_to_cache(user_id: int, auth_link: str) -> None:
        """Сохраняет ссылку авторизации в кеш"""
        expires_at = int(time.time()) + settings.AUTH_LINK_CACHE_TTL
        await cache_service.set_auth_link(user_id, auth_link, expires_at)

    @staticmethod
    async def generate_auth_link(
        user_id: int, username: Optional[str], phone: str
    ) -> dict:
        """Генерирует ссылку для авторизации"""
        try:
            response = await user_login(
                telegram_user_id=str(user_id),
                telegram_username=username,
                phone=phone,
            )

            # Сохраняем ссылку в кеш
            await AuthService.save_auth_link_to_cache(
                user_id, response["authorization_link"]
            )

            return response

        except (ClientConnectorError, ContentTypeError) as e:
            raise AuthError(f"Ошибка при генерации ссылки авторизации: {e}")

    @staticmethod
    def is_auth_link_valid(expires_at: int, current_time: Optional[int] = None) -> bool:
        """Проверяет, действительна ли ссылка авторизации"""
        if current_time is None:
            current_time = int(time.time())
        return current_time < expires_at
