from aiogram import BaseMiddleware
from aiogram.types import Update, Message

from src.bot.handlers.keyboards.admin import ADMIN_KEYBOARDS
from src.bot.handlers.keyboards.user import USER_KEYBOARDS
from src.bot.handlers.keyboards.worker import WORKER_KEYBOARDS
from src.bot.handlers.messages.admin import ADMIN_MESSAGES
from src.bot.handlers.messages.user import USER_MESSAGES
from src.bot.handlers.messages.worker import WORKER_MESSAGES


class LanguageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        message: Message = event.message
        lang = "ru"
        if message is not None:
            lang = message.from_user.language_code or lang

        if lang not in USER_MESSAGES.keys():
            lang = "ru"

        data["user_messages"] = USER_MESSAGES[lang]
        data["user_keyboards"] = USER_KEYBOARDS[lang]
        data["admin_messages"] = ADMIN_MESSAGES[lang]
        data["admin_keyboards"] = ADMIN_KEYBOARDS[lang]
        data["worker_messages"] = WORKER_MESSAGES[lang]
        data["worker_keyboards"] = WORKER_KEYBOARDS[lang]
        return await handler(event, data)
