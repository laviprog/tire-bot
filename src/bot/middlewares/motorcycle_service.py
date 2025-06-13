from advanced_alchemy.config import SQLAlchemyAsyncConfig
from aiogram import BaseMiddleware
from aiogram.types import Update

from src.motorcycles import MotorcycleService


class MotorcycleServiceMiddleware(BaseMiddleware):
    def __init__(self, config: SQLAlchemyAsyncConfig):
        super().__init__()
        self.config = config

    async def __call__(self, handler, event: Update, data: dict):
        async with MotorcycleService.new(config=self.config) as service:
            data["motorcycle_service"] = service
            return await handler(event, data)
