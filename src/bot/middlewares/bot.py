from aiogram import BaseMiddleware
from aiogram.types import Update


class BotMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        data["bot"] = data.get("bots")[0]
        return await handler(event, data)
