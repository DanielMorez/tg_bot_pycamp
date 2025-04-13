from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, KeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.keyboards import messages
from src.services.auth import user_login

router = Router()


# Состояния FSM
class AuthState(StatesGroup):
    waiting_for_phone = State()


@router.message(Command('start'))
async def start_command(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🔐Авторизоваться', callback_data='auth', request_contact=True))

    builder.add(
        InlineKeyboardButton(
            text='💬Чат с поддержкой',
            url='https://t.me/your_support_bot',  # Замените на ссылку на бота поддержки
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='🦊Наш канал',
            url='https://t.me/codelis_digest',  # Замените на ссылку на бота поддержки
        )
    )
    builder.add(
        InlineKeyboardButton(
            text='⁉️Вопросы и ответы',
            callback_data='faq',
        )
    )

    builder.adjust(1, 2, 1)

    await message.answer(messages.START, reply_markup=builder.as_markup())


@router.callback_query(F.data == 'auth')
async def auth_callback(callback: types.CallbackQuery, state: FSMContext):
    # TODO: здесь предусмотреть логику забор номера телефона из кэша

    # TODO: здесь проверять, если пользователь получал меньше 10 минут назад ссылку на авторизацию,
    #  то можно ее закешировать и вернуть.

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Поделиться номером телефона 📱', request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await callback.message.delete()

    # Запрашиваем номер телефона
    await callback.message.answer(messages.ASK_4_PHONE, reply_markup=keyboard)
    await state.set_state(AuthState.waiting_for_phone)


# Хэндлер для получения номера телефона
@router.message(AuthState.waiting_for_phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    # Получаем номер телефона из контакта
    phone_number = message.contact.phone_number

    # Сохраняем номер телефона в состоянии (если нужно)
    await state.update_data(phone=phone_number)

    loading_sticker = await message.answer_sticker(
        'CAACAgIAAxkBAAExqU9nq5ox8OKuKAR3gVTbqlxsOocsYAACeBsAArZjKElJPqq2J-v4QTYE'
    )
    loading_message = await message.answer(
        'Генерируем ссылку...',
        reply_markup=types.ReplyKeyboardRemove(),  # Убираем клавиатуру
    )

    response = await user_login(
        telegram_user_id=str(message.from_user.id),
        telegram_username=message.from_user.username,
        phone=phone_number,
    )

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='🔑 Ссылка для авторизации',
            url=response['authorization_link'],  # Замените на ссылку на бота поддержки
        )
    )

    await loading_message.delete()
    await loading_sticker.delete()

    await message.answer(messages.AUTH_LINK, reply_markup=builder.as_markup())


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
