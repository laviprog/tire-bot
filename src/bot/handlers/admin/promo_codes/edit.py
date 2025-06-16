from datetime import datetime
from uuid import UUID

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from src import log
from src.bot.handlers.utils import validate_datetime
from src.promo_codes import DiscountType, PromoCodeService, PromoCodeModel

router = Router()


class PromoCodeUpdate(StatesGroup):
    code = State()
    discount = State()
    valid_from = State()
    valid_until = State()
    usage_limit = State()


@router.callback_query(lambda callback_name: callback_name.data.startswith("edit_promo_code:"))
async def edit_promo_code_callback(
    callback: CallbackQuery, bot: Bot, state: FSMContext, promo_code_service: PromoCodeService
):
    promo_code_id = callback.data.split(":")[1]

    try:
        promo_code = await promo_code_service.get(promo_code_id)
    except Exception as e:
        await callback.answer(
            text="К сожалению, не удалось найти промокод. Попробуйте позже.", show_alert=True
        )
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
        text=f"Текущий код: {promo_code.code}\nНапиши новый код (например, SUM25) или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(PromoCodeUpdate.code))
async def code_process(message: Message, state: FSMContext):
    code = message.text.strip()

    if code != "Оставить без изменения":
        await state.update_data(code=code)

    data = await state.get_data()
    discount_type, discount_value = data.get("discount_type"), data.get("discount_value")

    await state.set_state(PromoCodeUpdate.discount)

    await message.answer(
        text=f"Текущая скидка: {discount_value}{'%' if discount_type == DiscountType.PERCENTAGE else ''}\n"
        f"Напиши новую скидку. Если ты хочешь сделать промокод с фиксированной скидкой (в рублях), просто напиши сумму без знака процента. Например: 25% или 1000. Если же хочешь ставить без изменений, то нажми на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(PromoCodeUpdate.discount))
async def discount_process(message: Message, state: FSMContext):
    discount = message.text.strip()

    if discount != "Оставить без изменения":
        discount_type = DiscountType.PERCENTAGE if discount.endswith("%") else DiscountType.FIXED
        discount_value = discount[:-1] if discount.endswith("%") else discount

        if not discount_value.isdigit():
            await message.answer(
                text="Пожалуйста, введи корректный размер скидки. Если это процент, напиши с символом '%', например: 25%. Если это фиксированная сумма, просто укажи число, например: 1000.",
                reply_markup=None,
            )
            return
        await state.update_data(discount_type=discount_type, discount_value=float(discount_value))

    data = await state.get_data()
    valid_from = data.get("valid_from")

    await state.set_state(PromoCodeUpdate.valid_from)
    await message.answer(
        text=(
            f"Сейчас промокод действует с {valid_from.strftime('%d.%m.%Y %H:%M')}"
            if valid_from
            else "Сейчас промокод не имеет начала действия"
        )
        + f"Укажи новое начало действия промокода (например, 30.07.2025 12:30 или 30.07.2025 (в таком случае промокод начнет действовать с начала дня)) или поставь -, если промокод не должен иметь начала действия, или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(PromoCodeUpdate.valid_from))
async def valid_from_process(message: Message, state: FSMContext):
    valid_from = message.text.strip()

    if valid_from != "Оставить без изменения":
        if valid_from in "-–":
            valid_from = None
        else:
            try:
                valid_from = validate_datetime(valid_from)
            except ValueError:
                await message.answer(
                    text="Пожалуйста, введи корректную дату в формате ДД.ММ.ГГГГ ЧЧ:ММ или ДД.ММ.ГГГГ, либо поставьте -",
                    reply_markup=None,
                )
                return
        await state.update_data(valid_from=valid_from.isoformat() if valid_from else None)

    data = await state.get_data()
    valid_until = data.get("valid_until")

    await state.set_state(PromoCodeUpdate.valid_until)
    await message.answer(
        text=(
            f"Сейчас промокод действует до {valid_until.strftime('%d.%m.%Y %H:%M')}"
            if valid_until
            else "Сейчас промокод не имеет окончания действия"
        )
        + f"Укажи новый конец действия промокода (например, 30.07.2025 12:30 или 30.07.2025 (в таком случае промокод начнет действовать с начала дня)) или поставь -, если промокод не должен иметь конца действия, или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(PromoCodeUpdate.valid_until))
async def valid_until_process(message: Message, state: FSMContext):
    valid_until = message.text.strip()

    if valid_until != "Оставить без изменения":
        if valid_until in "-–":
            valid_until = None
        else:
            try:
                valid_until = validate_datetime(valid_until)
            except ValueError:
                await message.answer(
                    text="Пожалуйста, введи корректную дату в формате ДД.ММ.ГГГГ ЧЧ:ММ или ДД.ММ.ГГГГ, либо поставьте -",
                    reply_markup=None,
                )
                return
        await state.update_data(valid_until=valid_until.isoformat() if valid_until else None)

    data = await state.get_data()
    usage_limit = data.get("usage_limit")

    await state.set_state(PromoCodeUpdate.usage_limit)
    await message.answer(
        text=f"Сейчас лимит использования промокода: {usage_limit if usage_limit is not None else 'нет ограничений'}\nУкажи новый лимит на количество использований промокода (например, 300 (в таком случае промокодом смогут воспользоваться первые 300 клиентов)) или поставь -, тогда не будет ограничений на количество использований промокода, или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(StateFilter(PromoCodeUpdate.usage_limit))
async def usage_limit_process(
    message: Message, state: FSMContext, promo_code_service: PromoCodeService
):
    usage_limit = message.text.strip()

    if usage_limit != "Оставить без изменения":
        if usage_limit in ("-", "–"):
            usage_limit = None
        else:
            try:
                usage_limit = int(message.text.strip())
            except ValueError:
                await message.answer(
                    text="Пожалуйста, введи корректное число (например, 234).", reply_markup=None
                )
                return

        if usage_limit and usage_limit < 0:
            await message.answer(
                text="Пожалуйста, убедись, что ты ввел корректное ограничение. PS: Ограничение не может быть меньше 0!",
                reply_markup=None,
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
                "valid_from": datetime.fromisoformat(data.get("valid_from")) if data.get("valid_from") else None,
                "valid_until": datetime.fromisoformat(data.get("valid_until")) if data.get('valid_until') else None,
                "usage_limit": data.get("usage_limit"),
            },
            item_id=UUID(data.get("id")),
        )
    except Exception as error:
        await message.answer(
            text="Произошла ошибка при обновлении промокода, пожалуйста, попробуйте позже",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Вернуться в начало ⬅️"),
                    ]
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
        log.error(f"Ошибка при обновлении промокода: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text="Промокод успешно обновлен!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Посмотреть промокоды ✅"),
                    KeyboardButton(text="Добавить промокод ➕"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ],
            ],
            resize_keyboard=True,
        ),
    )
