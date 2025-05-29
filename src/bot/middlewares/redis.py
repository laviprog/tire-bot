from aiogram import BaseMiddleware
from aiogram.types import Update

from redis.asyncio import Redis


class RedisMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis):
        super().__init__()
        self.redis = redis

    async def __call__(self, handler, event: Update, data: dict):
        data["redis"] = self.redis
        return await handler(event, data)
