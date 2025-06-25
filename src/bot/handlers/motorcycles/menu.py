from aiogram import Router, F
from aiogram.types import (
    Message,
)

from src.bot.handlers.keyboards.utils import CHECK_MOTORCYCLE, GARAGE
from src.motorcycles import MotorcycleService, MotorcycleModel

router = Router()


@router.message(*[F.text == text for text in GARAGE])
async def garage_command(message: Message, user_messages: dict, user_keyboards: dict):
    await message.answer(
        text=user_messages["garage"],
        reply_markup=user_keyboards["garage"],
    )


@router.message(*[F.text == text for text in CHECK_MOTORCYCLE])
async def view_motorcycles(
    message: Message,
    motorcycle_service: MotorcycleService,
    user_messages: dict,
    user_keyboards: dict,
):
    telegram_id = str(message.from_user.id)

    motorcycles = await motorcycle_service.list(MotorcycleModel.user_telegram_id == telegram_id)

    if not motorcycles:
        await message.answer(
            text=user_messages["garage_is_empty"],
        )
        return

    for motorcycle in motorcycles:
        await message.answer(
            text=user_messages["motorcycle"](motorcycle.motorcycle_model, motorcycle.year),
            reply_markup=user_keyboards["motorcycle"](motorcycle.id),
        )
