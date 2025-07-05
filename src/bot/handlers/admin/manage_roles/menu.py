from aiogram import Router
from aiogram.types import Message

from src.bot.filters import Text, IsAdmin
from src.bot.handlers.keyboards import MANAGE_ROLES

router = Router()


@router.message(Text(MANAGE_ROLES), IsAdmin())
async def manage_roles_menu(message: Message, messages: dict, keyboards: dict):
    await message.answer(
        text=messages["manage_roles_menu"],
        reply_markup=keyboards["manage_roles_menu"],
    )
