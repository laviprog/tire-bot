from aiogram import BaseMiddleware, Bot
from aiogram.types import Update


class BotMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()

    async def __call__(self, handler, event: Update, data: dict):
        data["bot"] = self.bot
        return await handler(event, data)
