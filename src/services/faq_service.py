from typing import List, Optional

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.constants import (
    BUTTON_FAQ_BACK,
    BUTTON_FAQ_HOME,
    CALLBACK_FAQ_BACK,
    CALLBACK_FAQ_HOME,
    CALLBACK_FAQ_QUESTION,
    CALLBACK_FAQ_THEME,
)
from src.types import FAQ_DATA, FAQTheme


class FAQService:
    """Сервис для работы с FAQ"""

    @staticmethod
    def get_themes() -> List[FAQTheme]:
        """Получает список всех тем FAQ"""
        return FAQ_DATA

    @staticmethod
    def get_theme_by_index(theme_index: int) -> Optional[FAQTheme]:
        """Получает тему по индексу"""
        if 0 <= theme_index < len(FAQ_DATA):
            return FAQ_DATA[theme_index]
        return None

    @staticmethod
    def get_question_by_indices(
        theme_index: int, question_index: int
    ) -> Optional[dict]:
        """Получает вопрос по индексам темы и вопроса"""
        theme = FAQService.get_theme_by_index(theme_index)
        if theme and 0 <= question_index < len(theme["questions"]):
            return theme["questions"][question_index]
        return None

    @staticmethod
    def create_themes_keyboard() -> InlineKeyboardBuilder:
        """Создает клавиатуру со списком тем"""
        builder = InlineKeyboardBuilder()

        for i, theme in enumerate(FAQ_DATA):
            builder.add(
                InlineKeyboardButton(
                    text=theme["theme"], callback_data=f"{CALLBACK_FAQ_THEME}:{i}"
                )
            )

        builder.adjust(1)  # По одной кнопке в строке
        return builder

    @staticmethod
    def create_questions_keyboard(theme_index: int) -> InlineKeyboardBuilder:
        """Создает клавиатуру со списком вопросов темы"""
        builder = InlineKeyboardBuilder()

        theme = FAQService.get_theme_by_index(theme_index)
        if not theme:
            return builder

        for i, question in enumerate(theme["questions"]):
            builder.add(
                InlineKeyboardButton(
                    text=question["question"],
                    callback_data=f"{CALLBACK_FAQ_QUESTION}:{theme_index}:{i}",
                )
            )

        # Добавляем кнопки навигации
        builder.add(
            InlineKeyboardButton(text=BUTTON_FAQ_BACK, callback_data=CALLBACK_FAQ_BACK)
        )
        builder.add(
            InlineKeyboardButton(text=BUTTON_FAQ_HOME, callback_data=CALLBACK_FAQ_HOME)
        )

        builder.adjust(1)  # По одной кнопке в строке
        return builder

    @staticmethod
    def create_navigation_keyboard(theme_index: int) -> InlineKeyboardBuilder:
        """Создает клавиатуру навигации для ответа на вопрос"""
        builder = InlineKeyboardBuilder()

        # Кнопка "Назад к вопросам"
        builder.add(
            InlineKeyboardButton(
                text="⬅️ К вопросам", callback_data=f"{CALLBACK_FAQ_THEME}:{theme_index}"
            )
        )

        # Кнопка "Назад к темам"
        builder.add(
            InlineKeyboardButton(text=BUTTON_FAQ_BACK, callback_data=CALLBACK_FAQ_BACK)
        )

        # Кнопка "Главное меню"
        builder.add(
            InlineKeyboardButton(text=BUTTON_FAQ_HOME, callback_data=CALLBACK_FAQ_HOME)
        )

        builder.adjust(1)  # По одной кнопке в строке
        return builder

    @staticmethod
    def format_question_answer(question_data: dict) -> str:
        """Форматирует вопрос и ответ для отображения"""
        return f"❓ <b>{question_data['question']}</b>\n\n💬 {question_data['answer']}"

    @staticmethod
    def format_theme_title(theme: FAQTheme) -> str:
        """Форматирует заголовок темы"""
        return f"📚 <b>{theme['theme']}</b>\n\nВыберите интересующий вас вопрос:"
