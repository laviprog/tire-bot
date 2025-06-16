from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.users import UserService


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, user_service: UserService) -> bool:
        telegram_id = str(message.from_user.id)
        return await user_service.is_admin_by_telegram_id(telegram_id)
