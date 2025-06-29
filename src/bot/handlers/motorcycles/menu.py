from aiogram import Router
from aiogram.types import (
    Message,
)

from src.bot.filters import Text
from src.bot.handlers.keyboards import CHECK_MOTORCYCLE, GARAGE
from src.motorcycles import MotorcycleService, MotorcycleModel

router = Router()


@router.message(Text(GARAGE))
async def garage_command(message: Message, messages: dict, keyboards: dict):
    await message.answer(
        text=messages["garage"],
        reply_markup=keyboards["garage"],
    )


@router.message(Text(CHECK_MOTORCYCLE))
async def view_motorcycles(
    message: Message,
    motorcycle_service: MotorcycleService,
    messages: dict,
    keyboards: dict,
):
    telegram_id = str(message.from_user.id)

    motorcycles = await motorcycle_service.list(MotorcycleModel.user_telegram_id == telegram_id)

    if not motorcycles:
        await message.answer(
            text=messages["garage_is_empty"],
        )
        return

    for motorcycle in motorcycles:
        await message.answer(
            text=messages["motorcycle"](motorcycle.motorcycle_model, motorcycle.year),
            reply_markup=keyboards["motorcycle"](motorcycle.id),
        )
