from aiogram import Router, F
from aiogram.types import Message

from src.bot.handlers.command import start_command

router = Router()


@router.message(F.text == "Вернуться в начало ⬅️")
async def back_to_start(message: Message):
    await start_command(message, "Чем я могу помочь тебе? Выбери действие из меню ниже:")
