from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.bot.filters import IsAdmin
from src.promo_codes import PromoCodeService, DiscountType

router = Router()


# @router.message(IsAdmin(), F.text == "Промокоды 💳")
# async def menu(message: Message):
#     await message.answer(
#         text="Выберите действие с промокодами:",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=[
#                 [
#                     KeyboardButton(text="Посмотреть промокоды ✅"),
#                     KeyboardButton(text="Добавить промокод ➕"),
#                     KeyboardButton(text="Вернуться в начало ⬅️"),
#                 ],
#             ],
#             resize_keyboard=True,
#         ),
#     )
#
#
# @router.message(IsAdmin(), F.text == "Посмотреть промокоды ✅")
# async def view_promo_codes(message: Message, promo_code_service: PromoCodeService):
#     promo_codes = await promo_code_service.list()
#
#     if not promo_codes:
#         await message.answer(
#             "На текущий момент нет промокодов. Добавьте новые промокоды, нажав на кнопку ниже."
#         )
#         return
#
#     for code in promo_codes:
#         await message.answer(
#             text=(
#                 f"Промокод: {code.code}\n"
#                 f"Скидка: {int(code.discount_value)}{'%' if code.discount_type == DiscountType.PERCENTAGE else ' руб.'}\n"
#                 f"Количество использований: {code.used_count}\n"
#             ),
#             reply_markup=InlineKeyboardMarkup(
#                 inline_keyboard=[
#                     [
#                         InlineKeyboardButton(
#                             text="Изменить промокод ✏️", callback_data=f"edit_promo_code:{code.id}"
#                         ),
#                         InlineKeyboardButton(
#                             text="Удалить промокод ❌",
#                             callback_data=f"delete_promo_code:{code.id}",
#                         ),
#                     ],
#                 ],
#                 resize_keyboard=True,
#             ),
#         )
