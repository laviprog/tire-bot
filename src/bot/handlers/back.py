from aiogram import Router, F
from aiogram.types import Message

from src.bot.handlers.keyboards.utils import BACK_TO_START
from src.users import UserService, Role

router = Router()


@router.message(*[F.text == back for back in BACK_TO_START])
async def back_to_start(
    message: Message,
    user_service: UserService,
    user_messages: dict,
    user_keyboards: dict,
    admin_keyboards: dict,
    worker_keyboards: dict,
):
    telegram_id = str(message.from_user.id)
    role = await user_service.get_role_by_telegram_id(telegram_id=telegram_id)
    text = user_messages["back_to_start"]

    match role:
        case Role.USER:
            await message.answer(
                text=text,
                reply_markup=user_keyboards["user_main_menu"],
            )
        case Role.WORKER:
            await message.answer(
                text=text,
                reply_markup=worker_keyboards["worker_main_menu"],
            )
        case Role.ADMIN:
            await message.answer(
                text=text,
                reply_markup=admin_keyboards["admin_main_menu"],
            )
        case _:
            await message.answer(
                text=text,
                reply_markup=user_keyboards["user_main_menu"],
            )
