from uuid import UUID

from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from src import log
from src.bot.handlers.back import back_to_start
from src.bot.handlers.keyboards.utils import LEAVE_UNCHANGED
from src.motorcycles import MotorcycleService
from src.users import UserService

router = Router()


class MotorcycleUpdate(StatesGroup):
    motorcycle_model = State()
    year = State()


@router.callback_query(lambda callback_name: callback_name.data.startswith("edit_motorcycle:"))
async def edit_motorcycle_callback(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    motorcycle_service: MotorcycleService,
    user_messages: dict,
    user_keyboards: dict,
):
    motorcycle_id = callback.data.split(":")[1]

    try:
        motorcycle = await motorcycle_service.get(motorcycle_id)
    except Exception as e:
        await callback.answer(text=user_messages["motorcycle_not_found_error"], show_alert=True)
        log.error(f"Ошибка при получении мотоцикла с ID {motorcycle_id}: {e}")
        return

    await state.update_data(
        id=str(motorcycle.id),
        motorcycle_model=motorcycle.motorcycle_model,
        year=motorcycle.year,
    )
    await state.set_state(MotorcycleUpdate.motorcycle_model)
    await callback.message.delete()
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=user_messages["edit_motorcycle_model_process"](motorcycle.motorcycle_model),
        reply_markup=user_keyboards["leave_unchanged"],
    )


@router.message(StateFilter(MotorcycleUpdate.motorcycle_model))
async def motorcycle_update_model_process(
    message: Message, state: FSMContext, user_messages: dict, user_keyboards: dict
):
    model = message.text.strip()

    if model not in LEAVE_UNCHANGED:
        await state.update_data(motorcycle_model=model)

    data = await state.get_data()
    motorcycle_year = data["year"]

    await state.set_state(MotorcycleUpdate.year)
    await message.answer(
        text=user_messages["edit_motorcycle_year_process"](motorcycle_year),
        reply_markup=user_keyboards["leave_unchanged"],
    )


@router.message(StateFilter(MotorcycleUpdate.year))
async def motorcycle_update_year_process(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    motorcycle_service: MotorcycleService,
    user_messages: dict,
    user_keyboards: dict,
    admin_keyboards: dict,
    worker_keyboards: dict,
):
    year = message.text.strip()

    if year not in LEAVE_UNCHANGED:
        try:
            year = int(message.text.strip())
        except ValueError:
            await message.answer(
                text=user_messages["not_valid_year"],
            )
            return

        if year < 1930 or year > 2025:
            await message.answer(
                text=user_messages["not_valid_year"],
            )
            return

        await state.update_data(year=year)

    data = await state.get_data()

    motorcycle_model = data["motorcycle_model"]
    motorcycle_year = data["year"]
    motorcycle_id = data["id"]

    try:
        await motorcycle_service.update(
            data={
                "motorcycle_model": motorcycle_model,
                "year": motorcycle_year,
            },
            item_id=UUID(motorcycle_id),
        )
    except Exception as error:
        await message.answer(
            text=user_messages["edit_motorcycle_error"],
        )
        await back_to_start(
            message, user_service, user_messages, user_keyboards, admin_keyboards, worker_keyboards
        )
        log.error(f"Ошибка при обновлении мотоцикла: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text=user_messages["motorcycle"](motorcycle_model, motorcycle_year),
        reply_markup=user_keyboards["motorcycle"](motorcycle_id),
    )

    await back_to_start(
        message, user_service, user_messages, user_keyboards, admin_keyboards, worker_keyboards
    )
