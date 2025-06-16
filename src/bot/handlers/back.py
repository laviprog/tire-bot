from aiogram import Router, F
from aiogram.types import Message

from src.bot.handlers.command import start_command
from src.users import UserService

router = Router()


@router.message(F.text == "Вернуться в начало ⬅️")
async def back_to_start(message: Message, user_service: UserService):
    await start_command(
        message, user_service, "Чем я могу помочь тебе? Выбери действие из меню ниже:"
    )
