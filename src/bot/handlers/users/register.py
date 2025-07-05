from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.bot.utils import is_valid_phone_number
from src.users import UserService, UserModel

router = Router()


class UserInfo(StatesGroup):
    name = State()
    phone_number = State()


async def create_profile_start(
    message: Message, state: FSMContext, user_service: UserService, messages: dict
):
    telegram_id = str(message.from_user.id)
    username = message.from_user.username
    chat_id = str(message.chat.id)

    await user_service.create(
        UserModel(
            telegram_id=telegram_id,
            username=username,
            chat_id=chat_id,
        )
    )

    await state.set_state(UserInfo.name)
    await message.answer(messages["register_name"])


@router.message(StateFilter(UserInfo.name))
async def process_name(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    messages: dict,
    keyboards: dict,
):
    name = message.text
    telegram_id = str(message.from_user.id)

    user = await user_service.get_by_telegram_id(telegram_id)
    user.name = name
    await user_service.update(user)
    await state.set_state(UserInfo.phone_number)
    await message.answer(
        text=messages["register_phone_number"], reply_markup=keyboards["request_contact"]
    )


@router.message(StateFilter(UserInfo.phone_number))
async def process_phone_number(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    messages: dict,
    keyboards: dict,
):
    from src.bot.handlers.commands import profile_command

    phone_number = message.contact.phone_number if message.contact else message.text
    phone_number = phone_number.strip().replace(" ", "")

    if not is_valid_phone_number(phone_number):
        await message.answer(messages["not_valid_phone_number"])
        return

    telegram_id = str(message.from_user.id)

    user = await user_service.get_by_telegram_id(telegram_id)
    user.phone_number = phone_number
    await user_service.update(user)

    await state.clear()
    await profile_command(message, user_service, messages, keyboards)
    await message.answer(
        text=messages["back_to_start"],
        reply_markup=keyboards["user_main_menu"],
    )
