from contextlib import asynccontextmanager

from redis.asyncio import Redis
from src.config import settings


@asynccontextmanager
async def redis_context():
    redis = Redis.from_url(settings.REDIS_URL)
    try:
        yield redis
    finally:
        await redis.close()
