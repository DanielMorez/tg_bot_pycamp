from aiogram import types, Router
from aiogram.filters import Command
from aiogram import Dispatcher

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я твой телеграм бот.")


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
