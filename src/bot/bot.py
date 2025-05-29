from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from src.bot.handlers.register_handlers import register_handlers
from src.bot.middlewares import RedisMiddleware
from src.config import settings
from src.redis import redis_context

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def run_bot():
    async with redis_context() as redis:
        storage = RedisStorage(redis)
        dp = Dispatcher(storage=storage)

        dp.update.middleware(RedisMiddleware(redis))

        register_handlers(dp)

        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()
