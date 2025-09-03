import time
from typing import Optional

from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings
from src.constants import (
    BUTTON_AUTH,
    BUTTON_AUTH_LINK,
    BUTTON_CHANNEL,
    BUTTON_FAQ,
    BUTTON_SHARE_PHONE,
    BUTTON_SUPPORT,
    CALLBACK_AUTH,
    CALLBACK_FAQ,
)
from src.keyboards import messages
from src.utils.readable_time import get_readable_expires


class UIService:
    """Сервис для работы с пользовательским интерфейсом"""

    @staticmethod
    def create_start_keyboard() -> InlineKeyboardBuilder:
        """Создает клавиатуру для команды /start"""
        builder = InlineKeyboardBuilder()

        builder.add(
            InlineKeyboardButton(
                text=BUTTON_AUTH, callback_data=CALLBACK_AUTH, request_contact=True
            )
        )
        builder.add(
            InlineKeyboardButton(
                text=BUTTON_SUPPORT,
                url=settings.SUPPORT_BOT_URL,
            )
        )
        builder.add(
            InlineKeyboardButton(
                text=BUTTON_CHANNEL,
                url=settings.CHANNEL_URL,
            )
        )
        builder.add(
            InlineKeyboardButton(
                text=BUTTON_FAQ,
                callback_data=CALLBACK_FAQ,
            )
        )

        builder.adjust(1, 2, 1)
        return builder

    @staticmethod
    def create_auth_link_keyboard(auth_link: str) -> InlineKeyboardBuilder:
        """Создает клавиатуру с ссылкой для авторизации"""
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=BUTTON_AUTH_LINK,
                url=auth_link,
            )
        )
        return builder

    @staticmethod
    def create_phone_request_keyboard() -> ReplyKeyboardMarkup:
        """Создает клавиатуру для запроса номера телефона"""
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=BUTTON_SHARE_PHONE, request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    @staticmethod
    def format_auth_link_message(
        expires_at: int, current_time: Optional[int] = None
    ) -> str:
        """Форматирует сообщение с информацией о времени действия ссылки"""
        if current_time is None:
            current_time = int(time.time())

        readable_time = get_readable_expires(expires_at, current_time)
        return f"⏰ Ссылка действительна еще {readable_time}"

    @staticmethod
    def format_auth_link_expires_message() -> str:
        """Возвращает сообщение о времени действия ссылки авторизации"""
        return messages.AUTH_LINK
