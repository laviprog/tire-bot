from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from src import log
from src.bot.filters import Text
from src.bot.handlers.keyboards import ADD_ADMIN, ADD_WORKER
from src.users import UserService, Role

router = Router()


class ManageRolesState(StatesGroup):
    admin_username = State()
    worker_username = State()


@router.message(Text(ADD_ADMIN))
async def add_admin_role(message: Message, state: FSMContext, messages: dict):
    await state.set_state(ManageRolesState.admin_username)
    await message.answer(
        text=messages["add_admin_username_process"], reply_markup=ReplyKeyboardRemove()
    )


@router.message(ManageRolesState.admin_username)
async def process_admin_username(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    messages: dict,
    keyboards: dict,
    bot: Bot,
):
    username = message.text.strip()
    username = username[1:] if username.startswith("@") else username

    try:
        user = await user_service.change_role(username=username, role=Role.ADMIN)
        chat_id = user.chat_id
        await message.answer(
            text=messages["admin_role_added"](user.username),
            reply_markup=keyboards["manage_roles_menu"],
        )
        await bot.send_message(
            chat_id=chat_id,
            text=messages["new_admin_role_notification"],
            reply_markup=keyboards["admin_main_menu"],
        )
    except ValueError:
        await message.answer(
            text=messages["user_not_found"](username), reply_markup=keyboards["manage_roles_menu"]
        )
    except Exception:
        await message.answer(
            text=messages["error_adding_admin"], reply_markup=keyboards["manage_roles_menu"]
        )
    finally:
        await state.clear()


@router.message(Text(ADD_WORKER))
async def add_worker_role(message: Message, state: FSMContext, messages: dict):
    await state.set_state(ManageRolesState.worker_username)
    await message.answer(
        text=messages["add_worker_username_process"], reply_markup=ReplyKeyboardRemove()
    )


@router.message(ManageRolesState.worker_username)
async def process_worker_username(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    messages: dict,
    keyboards: dict,
    bot: Bot,
):
    username = message.text.strip()
    username = username[1:] if username.startswith("@") else username
    try:
        user = await user_service.change_role(username=username, role=Role.WORKER)
        chat_id = user.chat_id
        await message.answer(
            text=messages["worker_role_added"](user.username),
            reply_markup=keyboards["manage_roles_menu"],
        )
        await bot.send_message(
            chat_id=chat_id,
            text=messages["new_worker_role_notification"],
            reply_markup=keyboards["worker_main_menu"],
        )
    except ValueError:
        await message.answer(text=messages["user_not_found"](username))
    except Exception as e:
        await message.answer(text=messages["error_adding_worker"])
        log.info(f"Error adding worker role for user {username}: {e}")
    finally:
        await state.clear()
