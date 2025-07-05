from aiogram import Router
from aiogram.types import Message

from src.bot.filters import IsAdmin, Text
from src.bot.handlers.keyboards import PROMO_CODES, CHECK_PROMO_CODES
from src.promo_codes import PromoCodeService

router = Router()


@router.message(IsAdmin(), Text(PROMO_CODES))
async def menu(message: Message, messages: dict, keyboards: dict):
    await message.answer(
        text=messages["promo_codes_menu"],
        reply_markup=keyboards["promo_codes_menu"],
    )


@router.message(IsAdmin(), Text(CHECK_PROMO_CODES))
async def view_promo_codes(
    message: Message, promo_code_service: PromoCodeService, messages: dict, keyboards: dict
):
    promo_codes = await promo_code_service.list()

    if not promo_codes:
        await message.answer(
            text=messages["no_promo_codes"],
        )
        return

    for code in promo_codes:
        await message.answer(
            text=messages["promo_code"](code),
            reply_markup=keyboards["promo_code_options"](code.id),
        )
