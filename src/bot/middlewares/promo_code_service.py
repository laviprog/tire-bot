from advanced_alchemy.config import SQLAlchemyAsyncConfig
from aiogram import BaseMiddleware
from aiogram.types import Update

from src.promo_codes import PromoCodeService


class PromoCodeServiceMiddleware(BaseMiddleware):
    def __init__(self, config: SQLAlchemyAsyncConfig):
        super().__init__()
        self.config = config

    async def __call__(self, handler, event: Update, data: dict):
        async with PromoCodeService.new(config=self.config) as service:
            data["promo_code_service"] = service
            return await handler(event, data)
