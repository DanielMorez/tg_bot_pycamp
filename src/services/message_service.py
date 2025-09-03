from typing import Optional

from aiogram import types
from config import settings


class MessageService:
    """Сервис для работы с сообщениями и уведомлениями"""

    @staticmethod
    async def send_loading_sticker(message: types.Message) -> Optional[types.Message]:
        """Отправляет стикер загрузки"""
        try:
            return await message.answer_sticker(settings.LOADING_STICKER_ID)
        except Exception:
            return None

    @staticmethod
    async def send_loading_message(message: types.Message) -> Optional[types.Message]:
        """Отправляет сообщение о загрузке"""
        try:
            return await message.answer(settings.LOADING_MESSAGE)
        except Exception:
            return None

    @staticmethod
    async def send_error_message(message: types.Message) -> None:
        """Отправляет сообщение об ошибке API"""
        await message.answer(settings.API_ERROR_MESSAGE)

    @staticmethod
    async def cleanup_messages(*messages: Optional[types.Message]) -> None:
        """Удаляет сообщения"""
        for msg in messages:
            if msg:
                try:
                    await msg.delete()
                except Exception:
                    pass
