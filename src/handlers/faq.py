from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import settings
from src.constants import (
    CALLBACK_AUTH,
    CALLBACK_FAQ,
    CALLBACK_FAQ_BACK,
    CALLBACK_FAQ_HOME,
    CALLBACK_FAQ_QUESTION,
    CALLBACK_FAQ_THEME,
)
from src.exceptions import AuthError
from src.keyboards import messages
from src.services.auth_service import AuthService
from src.services.faq_service import FAQService
from src.services.message_service import MessageService
from src.services.ui_service import UIService
from src.utils.logger import log_error, log_user_action, setup_logger

router = Router()
logger = setup_logger(__name__)


# Состояния FSM
class AuthState(StatesGroup):
    waiting_for_phone = State()


@router.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    log_user_action(logger, message.from_user, "started bot")
    keyboard = UIService.create_start_keyboard()
    await message.answer(messages.START, reply_markup=keyboard.as_markup())


@router.callback_query(F.data == CALLBACK_AUTH)
async def auth_callback(callback: types.CallbackQuery, state: FSMContext):
    """Обработчик нажатия кнопки авторизации"""
    log_user_action(logger, callback.from_user, "requested auth")
    user_id = callback.from_user.id

    # Проверяем кешированную ссылку авторизации
    cached_auth_data = await AuthService.get_cached_auth_link(user_id)

    if cached_auth_data and AuthService.is_auth_link_valid(
        cached_auth_data["expires_at"]
    ):
        await _handle_cached_auth_link(callback, cached_auth_data)
        return

    # Проверяем кешированный номер телефона
    cached_phone = await AuthService.get_cached_phone(user_id)

    if cached_phone:
        await _handle_cached_phone_auth(callback, cached_phone)
    else:
        await _request_phone_number(callback, state)


@router.callback_query(F.data == CALLBACK_FAQ)
async def faq_callback(callback: types.CallbackQuery):
    """Обработчик нажатия кнопки FAQ"""
    log_user_action(logger, callback.from_user, "opened FAQ")
    keyboard = FAQService.create_themes_keyboard()
    await callback.message.edit_text(
        messages.FAQ_WELCOME, reply_markup=keyboard.as_markup(), parse_mode="HTML"
    )


@router.callback_query(F.data.startswith(CALLBACK_FAQ_THEME))
async def faq_theme_callback(callback: types.CallbackQuery):
    """Обработчик выбора темы FAQ"""
    try:
        theme_index = int(callback.data.split(":")[1])
        theme = FAQService.get_theme_by_index(theme_index)

        if not theme:
            await callback.answer("Тема не найдена", show_alert=True)
            return

        log_user_action(
            logger, callback.from_user, "selected FAQ theme", theme=theme["theme"]
        )

        keyboard = FAQService.create_questions_keyboard(theme_index)
        await callback.message.edit_text(
            FAQService.format_theme_title(theme),
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML",
        )

    except (ValueError, IndexError):
        await callback.answer("Ошибка при выборе темы", show_alert=True)


@router.callback_query(F.data.startswith(CALLBACK_FAQ_QUESTION))
async def faq_question_callback(callback: types.CallbackQuery):
    """Обработчик выбора вопроса FAQ"""
    try:
        parts = callback.data.split(":")
        theme_index = int(parts[1])
        question_index = int(parts[2])

        question_data = FAQService.get_question_by_indices(theme_index, question_index)

        if not question_data:
            await callback.answer("Вопрос не найден", show_alert=True)
            return

        log_user_action(
            logger,
            callback.from_user,
            "viewed FAQ question",
            question=question_data["question"],
        )

        keyboard = FAQService.create_navigation_keyboard(theme_index)
        await callback.message.edit_text(
            FAQService.format_question_answer(question_data),
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML",
        )

    except (ValueError, IndexError):
        await callback.answer("Ошибка при выборе вопроса", show_alert=True)


@router.callback_query(F.data == CALLBACK_FAQ_BACK)
async def faq_back_callback(callback: types.CallbackQuery):
    """Обработчик кнопки 'Назад' в FAQ"""
    log_user_action(logger, callback.from_user, "went back in FAQ")
    keyboard = FAQService.create_themes_keyboard()
    await callback.message.edit_text(
        messages.FAQ_WELCOME, reply_markup=keyboard.as_markup(), parse_mode="HTML"
    )


@router.callback_query(F.data == CALLBACK_FAQ_HOME)
async def faq_home_callback(callback: types.CallbackQuery):
    """Обработчик кнопки 'Главное меню' в FAQ"""
    log_user_action(logger, callback.from_user, "returned to main menu from FAQ")
    keyboard = UIService.create_start_keyboard()
    await callback.message.edit_text(messages.START, reply_markup=keyboard.as_markup())


async def _handle_cached_auth_link(callback: types.CallbackQuery, auth_data: dict):
    """Обрабатывает кешированную ссылку авторизации"""
    import time

    current_time = int(time.time())
    expires_at = auth_data["expires_at"]

    message_text = UIService.format_auth_link_message(expires_at, current_time)
    keyboard = UIService.create_auth_link_keyboard(auth_data["link"])

    await callback.message.delete()
    await callback.message.answer(message_text, reply_markup=keyboard.as_markup())


async def _handle_cached_phone_auth(callback: types.CallbackQuery, phone: str):
    """Обрабатывает авторизацию с кешированным номером телефона"""
    loading_sticker = await MessageService.send_loading_sticker(callback.message)
    loading_message = await MessageService.send_loading_message(callback.message)

    try:
        response = await AuthService.generate_auth_link(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            phone=phone,
        )

        keyboard = UIService.create_auth_link_keyboard(response["authorization_link"])

        await MessageService.cleanup_messages(loading_message, loading_sticker)
        await callback.message.answer(
            UIService.format_auth_link_expires_message(),
            reply_markup=keyboard.as_markup(),
        )

    except AuthError as e:
        await MessageService.cleanup_messages(loading_message, loading_sticker)
        await MessageService.send_error_message(callback.message)
        log_error(logger, e, "auth link generation failed")


async def _request_phone_number(callback: types.CallbackQuery, state: FSMContext):
    """Запрашивает номер телефона у пользователя"""
    keyboard = UIService.create_phone_request_keyboard()

    await callback.message.delete()
    await callback.message.answer(messages.ASK_4_PHONE, reply_markup=keyboard)
    await state.set_state(AuthState.waiting_for_phone)


@router.message(AuthState.waiting_for_phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    """Обработчик получения номера телефона"""
    log_user_action(
        logger, message.from_user, "shared phone", phone=message.contact.phone_number
    )
    phone_number = message.contact.phone_number

    # Сохраняем номер телефона в кеш
    await AuthService.save_phone_to_cache(message.from_user.id, phone_number)

    # Сохраняем номер в состоянии
    await state.update_data(phone=phone_number)

    # Отправляем стикер и сообщение загрузки
    loading_sticker = await MessageService.send_loading_sticker(message)
    loading_message = await message.answer(
        settings.LOADING_MESSAGE,
        reply_markup=types.ReplyKeyboardRemove(),
    )

    try:
        response = await AuthService.generate_auth_link(
            user_id=message.from_user.id,
            username=message.from_user.username,
            phone=phone_number,
        )

        keyboard = UIService.create_auth_link_keyboard(response["authorization_link"])

        await MessageService.cleanup_messages(loading_message, loading_sticker)
        await message.answer(
            UIService.format_auth_link_expires_message(),
            reply_markup=keyboard.as_markup(),
        )

    except AuthError as e:
        await MessageService.cleanup_messages(loading_message, loading_sticker)
        await message.answer(
            settings.API_ERROR_MESSAGE, reply_markup=types.ReplyKeyboardRemove()
        )
        log_error(logger, e, "auth link generation failed")


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
