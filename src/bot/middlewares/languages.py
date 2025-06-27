from aiogram import BaseMiddleware
from aiogram.types import Update, Message

from src.bot.handlers.keyboards import KEYBOARDS
from src.bot.handlers.messages import MESSAGES


class LanguageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        message: Message = event.message
        lang = "ru"
        if message is not None:
            lang = message.from_user.language_code or lang

        if lang not in MESSAGES.keys():
            lang = "ru"

        data["messages"] = MESSAGES[lang]
        data["keyboards"] = KEYBOARDS[lang]

        return await handler(event, data)
