from aiogram import Router
from aiogram.types import Message

from src.bot.filters import Text
from src.bot.handlers.keyboards import BACK_TO_START
from src.users import UserService, Role

router = Router()


@router.message(Text(BACK_TO_START))
async def back_to_start(
    message: Message,
    user_service: UserService,
    messages: dict,
    keyboards: dict,
):
    telegram_id = str(message.from_user.id)
    role = await user_service.get_role_by_telegram_id(telegram_id=telegram_id)
    text = messages["back_to_start"]

    match role:
        case Role.USER:
            await message.answer(
                text=text,
                reply_markup=keyboards["user_main_menu"],
            )
        case Role.WORKER:
            await message.answer(
                text=text,
                reply_markup=keyboards["worker_main_menu"],
            )
        case Role.ADMIN:
            await message.answer(
                text=text,
                reply_markup=keyboards["admin_main_menu"],
            )
        case _:
            await message.answer(
                text=text,
                reply_markup=keyboards["user_main_menu"],
            )
