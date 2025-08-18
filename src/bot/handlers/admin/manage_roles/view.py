from aiogram import Router
from aiogram.types import Message

from src.bot.filters import Text
from src.bot.handlers.keyboards import LIST_ADMINS_AND_WORKERS
from src.users import UserService

router = Router()


@router.message(Text(LIST_ADMINS_AND_WORKERS))
async def list_admins_and_workers(message: Message, messages: dict, user_service: UserService):
    admins = await user_service.get_admins()
    workers = await user_service.get_workers()
    await message.answer(
        messages["list_admins_and_workers"](admins, workers),
    )
