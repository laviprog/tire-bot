from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.users import UserModel, UserService

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, user_service: UserService):
    await message.answer(f"Hi, your id: <code>{message.from_user.id}</code>")
    await user_service.create(
        UserModel(
            telegram_id=str(message.from_user.id),
            username=message.from_user.username,
        ),
        auto_commit=True,
    )
