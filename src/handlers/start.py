import logging

from aiogram import Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, KeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientConnectorError, ContentTypeError

from src.keyboards import messages
from src.services.auth import user_login
from src.services.cache import cache_service
from src.utils.readable_time import get_readable_expires

router = Router()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
    user_id = callback.from_user.id
    
    # Сначала проверяем кеш ссылок авторизации
    cached_auth_data = await cache_service.get_auth_link(user_id)
    
    if cached_auth_data:
        # Если ссылка есть в кеше, проверяем время истечения
        import time
        current_time = int(time.time())
        expires_at = cached_auth_data['expires_at']
        
        if current_time < expires_at:
            readable_time = get_readable_expires(expires_at, current_time)
            
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text='🔑 Ссылка для авторизации',
                    url=cached_auth_data['link'],
                )
            )
            
            await callback.message.delete()
            await callback.message.answer(
                f"⏰ Ссылка действительна еще {readable_time}",
                reply_markup=builder.as_markup()
            )
            return
    
    # Если ссылки нет в кеше или она истекла, проверяем номер телефона
    cached_phone = await cache_service.get_phone(user_id)
    
    if cached_phone:
        # Если номер есть в кеше, сразу генерируем ссылку для авторизации
        loading_sticker = await callback.message.answer_sticker(
            'CAACAgIAAxkBAAExqU9nq5ox8OKuKAR3gVTbqlxsOocsYAACeBsAArZjKElJPqq2J-v4QTYE'
        )
        loading_message = await callback.message.answer('Генерируем ссылку...')
        
        try:
            response = await user_login(
                telegram_user_id=str(callback.from_user.id),
                telegram_username=callback.from_user.username,
                phone=cached_phone,
            )
            
            # Сохраняем ссылку в кеш на 10 минут
            import time
            expires_at = int(time.time()) + 600  # 10 минут
            await cache_service.set_auth_link(user_id, response['authorization_link'], expires_at)
            
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text='🔑 Ссылка для авторизации',
                    url=response['authorization_link'],
                )
            )
            
            await loading_message.delete()
            await loading_sticker.delete()
            await callback.message.answer(messages.AUTH_LINK, reply_markup=builder.as_markup())
            
        except (ClientConnectorError, ContentTypeError) as e:
            await loading_message.delete()
            await loading_sticker.delete()
            await callback.message.answer(
                'Наш сервис сейчас немного прилёг отдохнуть — мы быстро чиним и перезагружаем,' 
                ' чтобы всё снова работало как часы🤕'
            )
            logger.error(f'Ошибка при отправке запроса или обработке ответа API: {e}')
            return
    else:
        # Если номера нет в кеше, запрашиваем его
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
    
    # Сохраняем номер телефона в кеше на 7 дней
    await cache_service.set_phone(message.from_user.id, phone_number)

    # Сохраняем номер телефона в состоянии (если нужно)
    await state.update_data(phone=phone_number)

    loading_sticker = await message.answer_sticker(
        'CAACAgIAAxkBAAExqU9nq5ox8OKuKAR3gVTbqlxsOocsYAACeBsAArZjKElJPqq2J-v4QTYE'
    )
    loading_message = await message.answer(
        'Генерируем ссылку...',
        reply_markup=types.ReplyKeyboardRemove(),  # Убираем клавиатуру
    )

    try:
        response = await user_login(
            telegram_user_id=str(message.from_user.id),
            telegram_username=message.from_user.username,
            phone=phone_number,
        )
        
        # Сохраняем ссылку в кеш на 10 минут
        import time
        expires_at = int(time.time()) + 600  # 10 минут
        await cache_service.set_auth_link(message.from_user.id, response['authorization_link'], expires_at)
        
    except (ClientConnectorError, ContentTypeError) as e:
        await loading_message.delete()
        await loading_sticker.delete()
        await message.answer(
            'Наш сервис сейчас немного прилёг отдохнуть — мы быстро чиним и перезагружаем,' 
            ' чтобы всё снова работало как часы🤕',
            reply_markup=types.ReplyKeyboardRemove(),  # Убираем клавиатуру
        )
        logger.error(f'Ошибка при отправке запроса или обработке ответа API: {e}')
        return

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
