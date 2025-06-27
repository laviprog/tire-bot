from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from src import log
from src.bot.handlers.utils import validate_datetime
from src.promo_codes import DiscountType, PromoCodeService, PromoCodeModel

router = Router()


class PromoCodeCreate(StatesGroup):
    code = State()
    discount = State()
    valid_from = State()
    valid_until = State()
    usage_limit = State()


# @router.message(F.text == "Добавить промокод ➕")
# async def start_create(message: Message, state: FSMContext):
#     await message.answer(
#         text="Супер! Давай начнем добавление нового промокода.\nНапиши мне код промокода (например, SUMMER2023)",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#     await state.set_state(PromoCodeCreate.code)
#
#
# @router.message(StateFilter(PromoCodeCreate.code))
# async def code_process(message: Message, state: FSMContext):
#     promo_code = message.text.strip()
#     await state.update_data(code=promo_code)
#
#     await message.answer(
#         text="Суперский промокод! Теперь напиши размер скидки (есть два вида: в процентах или в рублях).\n"
#         "Если ты хочешь сделать промокод с фиксированной скидкой (в рублях), просто напиши сумму без знака процента. Например: 25% или 1000.",
#     )
#
#     await state.set_state(PromoCodeCreate.discount)
#
#
# @router.message(StateFilter(PromoCodeCreate.discount))
# async def discount_process(message: Message, state: FSMContext):
#     discount = message.text.strip()
#     discount_type = DiscountType.PERCENTAGE if discount.endswith("%") else DiscountType.FIXED
#     discount_value = discount[:-1] if discount.endswith("%") else discount
#
#     if not discount_value.isdigit():
#         await message.answer(
#             text="Пожалуйста, введи корректный размер скидки. Если это процент, напиши с символом '%', например: 25%. Если это фиксированная сумма, просто укажи число, например: 1000.",
#         )
#         return
#
#     await state.update_data(
#         discount_type=discount_type,
#         discount_value=float(discount_value),
#     )
#
#     await message.answer(
#         text="Отлично! Теперь напиши с какого времени будет действовать промокод (например, 30.07.2025 12:30 или 30.07.2025 (в таком случае промокод начнет действовать с начала дня)) или поставь -, если промокод не должен иметь начала действия",
#     )
#
#     await state.set_state(PromoCodeCreate.valid_from)
#
#
# @router.message(StateFilter(PromoCodeCreate.valid_from))
# async def valid_from_process(message: Message, state: FSMContext):
#     valid_from = message.text.strip()
#
#     if valid_from in "-–":
#         valid_from = None
#     else:
#         try:
#             valid_from = validate_datetime(valid_from)
#         except ValueError:
#             await message.answer(
#                 text="Пожалуйста, введи корректную дату в формате ДД.ММ.ГГГГ ЧЧ:ММ или ДД.ММ.ГГГГ, либо поставьте -",
#             )
#             return
#
#     await state.update_data(valid_from=valid_from.isoformat() if valid_from else None)
#
#     await message.answer(
#         text="Хорошо! Теперь напиши до какого времени будет действовать промокод (например, 30.07.2025 12:30 или 30.07.2025 (в таком случае промокод будет действовать до 29.07.2025 23:59)) или поставь -, если промокод не должен иметь конца действия",
#     )
#
#     await state.set_state(PromoCodeCreate.valid_until)
#
#
# @router.message(StateFilter(PromoCodeCreate.valid_until))
# async def valid_until_process(message: Message, state: FSMContext):
#     valid_until = message.text.strip()
#
#     if valid_until in "-–":
#         valid_until = None
#     else:
#         try:
#             valid_until = validate_datetime(valid_until)
#         except ValueError:
#             await message.answer(
#                 text="Пожалуйста, введи корректную дату в формате ДД.ММ.ГГГГ ЧЧ:ММ или ДД.ММ.ГГГГ, либо поставьте -",
#             )
#             return
#
#     await state.update_data(valid_until=valid_until.isoformat() if valid_until else None)
#
#     await message.answer(
#         text="Отлично! Теперь можно указать лимит на количество использований промокода (например, 300 (в таком случае промокодом смогут воспользоваться первые 300 клиентов)) или поставьте -, тогда не будет ограничений на количество использований промокода",
#     )
#
#     await state.set_state(PromoCodeCreate.usage_limit)
#
#
# @router.message(StateFilter(PromoCodeCreate.usage_limit))
# async def motorcycle_year_process(
#     message: Message, state: FSMContext, promo_code_service: PromoCodeService
# ):
#     usage_limit = message.text.strip()
#
#     if usage_limit in ("-", "–"):
#         usage_limit = None
#     else:
#         try:
#             usage_limit = int(message.text.strip())
#         except ValueError:
#             await message.answer(
#                 text="Пожалуйста, введи корректное число (например, 234).", reply_markup=None
#             )
#             return
#
#     if usage_limit and usage_limit < 0:
#         await message.answer(
#             text="Пожалуйста, убедись, что ты ввел корректное ограничение. PS: Ограничение не может быть меньше 0!",
#         )
#         return
#
#     data = await state.get_data()
#
#     promo_code = PromoCodeModel(
#         code=data.get("code"),
#         discount_type=data.get("discount_type"),
#         discount_value=data.get("discount_value"),
#         valid_from=datetime.fromisoformat(data.get("valid_from"))
#         if data.get("valid_from")
#         else None,
#         valid_until=datetime.fromisoformat(data.get("valid_until"))
#         if data.get("valid_until")
#         else None,
#         usage_limit=usage_limit,
#     )
#     try:
#         await promo_code_service.create(promo_code)
#     except Exception as error:
#         await message.answer(
#             text="Произошла ошибка при добавлении промокода, пожалуйста, попробуйте позже",
#             reply_markup=ReplyKeyboardMarkup(
#                 keyboard=[
#                     [
#                         KeyboardButton(text="Вернуться в начало ⬅️"),
#                     ]
#                 ],
#                 resize_keyboard=True,
#             ),
#         )
#         log.error(f"Ошибка при создании промокода: {error}")
#         return
#     finally:
#         await state.clear()
#
#     await message.answer(
#         text="Промокод успешно добавлен!",
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
