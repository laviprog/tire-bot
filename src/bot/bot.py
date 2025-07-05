from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis import Redis

from src.bot.handlers import register_handlers
from src.bot.middlewares import register_middlewares
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

        register_middlewares(dp, redis=redis)
        register_handlers(dp)

        await base_settings(redis)

        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()


async def base_settings(redis: Redis):
    if not await redis.exists("max_records"):
        await redis.set("max_records", settings.MAX_RECORDS)
    if not await redis.exists("operating_mode"):
        await redis.set("operating_mode", settings.OPERATING_MODE)
