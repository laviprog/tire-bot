from uuid import UUID

from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from src import log
from src.bot.utils import is_valid_phone_number
from src.users import UserService

router = Router()


class UserUpdate(StatesGroup):
    name = State()
    phone_number = State()


@router.callback_query(lambda callback: callback.data.startswith("edit_user:"))
async def edit_user_callback(
    callback: CallbackQuery, bot: Bot, state: FSMContext, user_service: UserService
):
    user_id = callback.data.split(":")[1]

    try:
        user = await user_service.get(user_id)
    except Exception as e:
        await callback.answer(
            text="К сожалению, не удалось найти профиль. Попробуйте позже.", show_alert=True
        )
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
        text=f"Ваше текущее имя: {user.name}\nНапиши новое имя или оставь без изменений, нажав на кнопку ниже.",
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


@router.message(StateFilter(UserUpdate.name))
async def update_name(message: Message, state: FSMContext):
    name = message.text.strip()

    if not name == "Оставить без изменения":
        await state.update_data(name=name)

    data = await state.get_data()
    phone_number = data["phone_number"]

    await state.set_state(UserUpdate.phone_number)

    await message.answer(
        text=f"Ваш текущий номер телефона: {phone_number}\nВведите новый номер телефона или нажмите кнопку ниже для отправки контакта или для того, чтобы оставить номер телефона без изменения.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Отправить номер телефона", request_contact=True),
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(UserUpdate.phone_number))
async def update_phone_number(message: Message, state: FSMContext, user_service: UserService):
    if not message.text == "Оставить без изменения":
        if message.contact:
            phone_number = message.contact.phone_number
        else:
            phone_number = message.text.strip()

        if not is_valid_phone_number(phone_number):
            await message.answer("Пожалуйста, введите корректный номер телефона.")
            return

        await state.update_data(phone_number=phone_number)

    data = await state.get_data()

    try:
        await user_service.update(
            data={
                "name": data["name"],
                "phone_number": data["phone_number"],
            },
            item_id=UUID(data["id"]),
        )
    except Exception as error:
        await message.answer(
            text="Произошла ошибка при обновлении пользователя, пожалуйста, попробуйте позже",
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
        log.error(f"Ошибка при обновлении мотоцикла: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text="Твой профиль успешно обновлен!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Мой профиль 👤"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )
