from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)

from src.bot.filters import IsUser, IsAdmin, IsWorker
from src.bot.handlers.keyboards import PROFILES
from src.bot.handlers.users.register import create_profile_start
from src.users import UserService

router = Router()


@router.message(IsUser(), CommandStart())
async def start_command_user(message: Message, messages: dict, keyboards: dict):
    await message.answer(
        text=messages["user_start_message"],
        reply_markup=keyboards["user_main_menu"],
    )


@router.message(IsAdmin(), CommandStart())
async def start_command_admin(message: Message, messages: dict, keyboards: dict):
    await message.answer(
        text=messages["admin_start_message"], reply_markup=keyboards["admin_main_menu"]
    )


@router.message(IsWorker(), CommandStart())
async def start_command_worker(message: Message, messages: dict, keyboards: dict):
    await message.answer(
        text=messages["worker_start_message"],
        reply_markup=keyboards["worker_main_menu"],
    )


@router.message(CommandStart())
async def start_command(
    message: Message, messages: dict, state: FSMContext, user_service: UserService
):
    await message.answer(
        text=messages["new_user_start_message"],
        reply_markup=ReplyKeyboardRemove(),
    )
    await create_profile_start(message, state, user_service, messages)


@router.message(Command("help"))
async def help_command(message: Message, messages: dict):
    await message.answer(messages["help"])


@router.message(*[F.text == profile for profile in PROFILES])
@router.message(Command("profile"))
async def profile_command(
    message: Message, user_service: UserService, messages: dict, keyboards: dict
):
    telegram_id = str(message.from_user.id)
    user = await user_service.get_by_telegram_id(telegram_id)
    await message.answer(
        text=messages["profile"](user.name, user.phone_number),
        reply_markup=keyboards["profile"](user.id),
    )
