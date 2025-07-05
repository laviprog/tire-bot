from datetime import datetime, timezone
from uuid import UUID

from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from src import log
from src.bot.handlers.keyboards import LEAVE_UNCHANGED
from src.bot.handlers.utils import validate_datetime
from src.promo_codes import DiscountType, PromoCodeService

router = Router()


class PromoCodeUpdate(StatesGroup):
    code = State()
    discount = State()
    valid_from = State()
    valid_until = State()
    usage_limit = State()


@router.callback_query(lambda callback_name: callback_name.data.startswith("edit_promo_code:"))
async def edit_promo_code_callback(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    promo_code_service: PromoCodeService,
    messages: dict,
    keyboards: dict,
):
    promo_code_id = callback.data.split(":")[1]

    try:
        promo_code = await promo_code_service.get(promo_code_id)
    except Exception as e:
        await callback.answer(text=messages["promo_code_not_found"], show_alert=True)
        log.error(f"Ошибка при получении мотоцикла с ID {promo_code_id}: {e}")
        return

    await state.update_data(
        id=promo_code_id,
        code=promo_code.code,
        discount_type=promo_code.discount_type,
        discount_value=promo_code.discount_value,
        valid_from=promo_code.valid_from,
        valid_until=promo_code.valid_until,
        usage_limit=promo_code.usage_limit,
    )
    await state.set_state(PromoCodeUpdate.code)
    await callback.message.delete()
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=messages["edit_promo_code_start"](promo_code.code),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(PromoCodeUpdate.code))
async def code_process(message: Message, state: FSMContext, messages: dict, keyboards: dict):
    code = message.text.strip()

    if code not in LEAVE_UNCHANGED:
        await state.update_data(code=code)

    data = await state.get_data()
    discount_type, discount_value = data.get("discount_type"), data.get("discount_value")

    await state.set_state(PromoCodeUpdate.discount)

    await message.answer(
        text=messages["edit_promo_code_discount"](discount_value, discount_type),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(PromoCodeUpdate.discount))
async def discount_process(message: Message, state: FSMContext, messages: dict, keyboards: dict):
    discount = message.text.strip()

    if discount not in LEAVE_UNCHANGED:
        discount_type = DiscountType.PERCENTAGE if discount.endswith("%") else DiscountType.FIXED
        discount_value = discount[:-1] if discount.endswith("%") else discount

        if not discount_value.isdigit():
            await message.answer(
                text=messages["promo_code_discount_value_error"],
                reply_markup=keyboards["leave_unchanged"],
            )
            return
        await state.update_data(discount_type=discount_type, discount_value=float(discount_value))

    data = await state.get_data()
    valid_from = data.get("valid_from")

    await state.set_state(PromoCodeUpdate.valid_from)
    await message.answer(
        text=messages["edit_promo_code_valid_from"](valid_from),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(PromoCodeUpdate.valid_from))
async def valid_from_process(message: Message, state: FSMContext, messages: dict, keyboards: dict):
    valid_from = message.text.strip()

    if valid_from not in LEAVE_UNCHANGED:
        if valid_from in ("-", "–"):
            valid_from = None
        else:
            try:
                valid_from = validate_datetime(valid_from)
            except ValueError:
                await message.answer(
                    text=messages["promo_code_date_error"],
                    reply_markup=keyboards["leave_unchanged"],
                )
                return
        await state.update_data(valid_from=valid_from.isoformat() if valid_from else None)

    data = await state.get_data()
    valid_until = data.get("valid_until")

    await state.set_state(PromoCodeUpdate.valid_until)
    await message.answer(
        text=messages["edit_promo_code_valid_until"](valid_until),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(PromoCodeUpdate.valid_until))
async def valid_until_process(message: Message, state: FSMContext, messages: dict, keyboards: dict):
    valid_until = message.text.strip()

    if valid_until not in LEAVE_UNCHANGED:
        if valid_until in ("-", "–"):
            valid_until = None
        else:
            try:
                valid_until = validate_datetime(valid_until)
            except ValueError:
                await message.answer(
                    text=messages["promo_code_date_error"],
                    reply_markup=keyboards["leave_unchanged"],
                )
                return
        await state.update_data(valid_until=valid_until.isoformat() if valid_until else None)

    data = await state.get_data()
    usage_limit = data.get("usage_limit")

    await state.set_state(PromoCodeUpdate.usage_limit)
    await message.answer(
        text=messages["edit_promo_code_usage_limit"](usage_limit),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(PromoCodeUpdate.usage_limit))
async def usage_limit_process(
    message: Message,
    state: FSMContext,
    promo_code_service: PromoCodeService,
    messages: dict,
    keyboards: dict,
):
    usage_limit = message.text.strip()

    if usage_limit not in LEAVE_UNCHANGED:
        if usage_limit in ("-", "–"):
            usage_limit = None
        else:
            try:
                usage_limit = int(message.text.strip())
            except ValueError:
                await message.answer(
                    text=messages["promo_code_usage_limit_error"],
                    reply_markup=keyboards["leave_unchanged"],
                )
                return

        if usage_limit and usage_limit < 0:
            await message.answer(
                text=messages["promo_code_usage_limit_negative_error"],
                reply_markup=keyboards["leave_unchanged"],
            )
            return

        await state.update_data(usage_limit=usage_limit)

    data = await state.get_data()

    try:
        await promo_code_service.update(
            data={
                "code": data.get("code"),
                "discount_type": data.get("discount_type"),
                "discount_value": data.get("discount_value"),
                "valid_from": datetime.fromisoformat(data.get("valid_from")).replace(
                    tzinfo=timezone.utc
                )
                if data.get("valid_from")
                else None,
                "valid_until": datetime.fromisoformat(data.get("valid_until")).replace(
                    tzinfo=timezone.utc
                )
                if data.get("valid_until")
                else None,
                "usage_limit": data.get("usage_limit"),
            },
            item_id=UUID(data.get("id")),
        )
    except Exception as error:
        await message.answer(
            text=messages["promo_code_update_error"],
            reply_markup=keyboards["promo_codes_menu"],
        )
        log.error(f"Ошибка при обновлении промокода: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text=messages["edit_promo_code_successful"],
        reply_markup=keyboards["promo_codes_menu"],
    )
