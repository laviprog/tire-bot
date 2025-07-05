from datetime import datetime, timezone

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from src import log
from src.bot.filters import Text
from src.bot.handlers.keyboards import ADD_PROMO_CODE
from src.bot.handlers.utils import validate_datetime
from src.promo_codes import DiscountType, PromoCodeService, PromoCodeModel

router = Router()


class PromoCodeCreate(StatesGroup):
    code = State()
    discount = State()
    valid_from = State()
    valid_until = State()
    usage_limit = State()


@router.message(Text(ADD_PROMO_CODE))
async def start_create(message: Message, state: FSMContext, messages: dict):
    await message.answer(
        text=messages["start_create_promo_code"],
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(PromoCodeCreate.code)


@router.message(StateFilter(PromoCodeCreate.code))
async def code_process(message: Message, state: FSMContext, messages: dict):
    promo_code = message.text.strip()
    await state.update_data(code=promo_code)

    await message.answer(
        text=messages["discount_promo_code_process"],
    )

    await state.set_state(PromoCodeCreate.discount)


@router.message(StateFilter(PromoCodeCreate.discount))
async def discount_process(message: Message, state: FSMContext, messages: dict):
    discount = message.text.strip()
    discount_type = DiscountType.PERCENTAGE if discount.endswith("%") else DiscountType.FIXED
    discount_value = discount[:-1] if discount.endswith("%") else discount

    if not discount_value.isdigit():
        await message.answer(
            text=messages["promo_code_discount_value_error"],
        )
        return

    await state.update_data(
        discount_type=discount_type,
        discount_value=float(discount_value),
    )

    await message.answer(
        text=messages["promo_code_start_date_process"],
    )

    await state.set_state(PromoCodeCreate.valid_from)


@router.message(StateFilter(PromoCodeCreate.valid_from))
async def valid_from_process(message: Message, state: FSMContext, messages: dict):
    valid_from = message.text.strip()

    if valid_from in ("-", "–"):
        valid_from = None
    else:
        try:
            valid_from = validate_datetime(valid_from)
        except ValueError:
            await message.answer(
                text=messages["promo_code_date_error"],
            )
            return

    await state.update_data(valid_from=valid_from.isoformat() if valid_from else None)

    await message.answer(
        text=messages["promo_code_end_date_process"],
    )

    await state.set_state(PromoCodeCreate.valid_until)


@router.message(StateFilter(PromoCodeCreate.valid_until))
async def valid_until_process(message: Message, state: FSMContext, messages: dict):
    valid_until = message.text.strip()

    if valid_until in ("-", "–"):
        valid_until = None
    else:
        try:
            valid_until = validate_datetime(valid_until)
        except ValueError:
            await message.answer(
                text=messages["promo_code_date_error"],
            )
            return

    await state.update_data(valid_until=valid_until.isoformat() if valid_until else None)

    await message.answer(
        text=messages["promo_code_usage_limit_process"],
    )

    await state.set_state(PromoCodeCreate.usage_limit)


@router.message(StateFilter(PromoCodeCreate.usage_limit))
async def motorcycle_year_process(
    message: Message,
    state: FSMContext,
    promo_code_service: PromoCodeService,
    messages: dict,
    keyboards: dict,
):
    usage_limit = message.text.strip()

    if usage_limit in ("-", "–"):
        usage_limit = None
    else:
        try:
            usage_limit = int(message.text.strip())
        except ValueError:
            await message.answer(
                text=messages["promo_code_usage_limit_error"],
            )
            return

    if usage_limit and usage_limit < 0:
        await message.answer(
            text=messages["promo_code_usage_limit_negative_error"],
        )
        return

    data = await state.get_data()

    promo_code = PromoCodeModel(
        code=data.get("code"),
        discount_type=data.get("discount_type"),
        discount_value=data.get("discount_value"),
        valid_from=datetime.fromisoformat(data.get("valid_from")).replace(tzinfo=timezone.utc)
        if data.get("valid_from")
        else None,
        valid_until=datetime.fromisoformat(data.get("valid_until")).replace(tzinfo=timezone.utc)
        if data.get("valid_until")
        else None,
        usage_limit=usage_limit,
    )
    try:
        await promo_code_service.create(promo_code)
    except Exception as error:
        await message.answer(
            text=messages["promo_code_created_error"], reply_markup=keyboards["promo_codes_menu"]
        )
        log.error(f"Ошибка при создании промокода: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text=messages["promo_code_created_successful"], reply_markup=keyboards["promo_codes_menu"]
    )
