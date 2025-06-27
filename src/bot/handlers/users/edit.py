from uuid import UUID

from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from src import log
from src.bot.handlers.back import back_to_start
from src.bot.handlers.keyboards import LEAVE_UNCHANGED
from src.bot.utils import is_valid_phone_number
from src.users import UserService

router = Router()


class UserUpdate(StatesGroup):
    name = State()
    phone_number = State()


@router.callback_query(lambda callback: callback.data.startswith("edit_user:"))
async def edit_user_callback(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    user_service: UserService,
    messages: dict,
    keyboards: dict,
):
    user_id = callback.data.split(":")[1]

    try:
        user = await user_service.get(user_id)
    except Exception as e:
        await callback.answer(text=messages["could_not_find_user"], show_alert=True)
        log.error(f"Ошибка при получении пользователя {user_id}: {e}")
        return

    await state.update_data(
        id=str(user_id),
        name=user.name,
        phone_number=user.phone_number,
    )
    await state.set_state(UserUpdate.name)
    await callback.message.delete()

    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=messages["edit_name_process"](user.name),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(UserUpdate.name))
async def update_name(message: Message, state: FSMContext, messages: dict, keyboards: dict):
    name = message.text.strip()

    if name not in LEAVE_UNCHANGED:
        await state.update_data(name=name)

    data = await state.get_data()
    phone_number = data["phone_number"]

    await state.set_state(UserUpdate.phone_number)

    await message.answer(
        text=messages["edit_phone_number_process"](phone_number),
        reply_markup=keyboards["leave_unchanged_with_request_contact"],
    )


@router.message(StateFilter(UserUpdate.phone_number))
async def update_phone_number(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    messages: dict,
    keyboards: dict,
):
    if message.text not in LEAVE_UNCHANGED:
        if message.contact:
            phone_number = message.contact.phone_number
        else:
            phone_number = message.text.strip()

        if not is_valid_phone_number(phone_number):
            await message.answer(text=messages["not_valid_phone_number"])
            return

        await state.update_data(phone_number=phone_number)

    data = await state.get_data()

    name = data["name"]
    phone_number = data["phone_number"]
    user_id = data["id"]

    try:
        await user_service.update(
            data={
                "name": name,
                "phone_number": phone_number,
            },
            item_id=UUID(data["id"]),
        )
    except Exception as error:
        await message.answer(
            text=messages["error_user_update"], reply_markup=keyboards["user_main_menu"]
        )
        log.error(f"Ошибка при обновлении пользователя: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text=messages["profile"](name, phone_number),
        reply_markup=keyboards["profile"](user_id),
    )

    await back_to_start(message, user_service, messages, keyboards)
