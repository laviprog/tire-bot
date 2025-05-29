from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.bot.handlers.register_handlers import register_handlers
from src.config import settings

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def run_bot():
    dp = Dispatcher()

    register_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
