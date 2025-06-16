from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src import log
from src.users import UserService

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, user_service: UserService, text: str | None = None):
    if text:
        log.info(f"User {message.from_user.id} started the bot with text: {text}")

    if await user_service.is_admin_by_telegram_id(str(message.from_user.id)):
        await message.answer(
            text="Привет, админ!" if not text else text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Заявки 📋"),
                        KeyboardButton(text="Мастера 🛠️"),
                    ],
                    [
                        KeyboardButton(text="Промокоды 💳"),
                        KeyboardButton(text="Пользователи 👥"),
                    ],
                ],
                resize_keyboard=True,
            ),
        )

    else:
        await message.answer(
            text="Привет путник!\nЯ помогу тебе починить твой мот!" if not text else text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Вызвать эвакуатор 🚑"),
                        KeyboardButton(text="Записаться на сервис 🛠️"),
                    ],
                    [
                        KeyboardButton(text="Мой гараж 🏍️"),
                        KeyboardButton(text="Мой профиль 👤"),
                    ],
                ],
                resize_keyboard=True,
            ),
        )


@router.message(Command("help"))
async def help_comand(message: Message):
    await message.answer(
        text="Я помогу тебе починить твой мот!\n"
        "Вот список команд, которые я понимаю:\n"
        "/start - начать работу со мной\n"
        "/help - показать это сообщение\n"
        "/profile - показать информацию о тебе\n"
    )


@router.message(F.text == "Мой профиль 👤")
@router.message(Command("profile"))
async def profile_command(message: Message, user_service: UserService):
    telegram_id = str(message.from_user.id)

    user = await user_service.get_by_telegram_id(telegram_id)

    if not user:
        await message.answer(
            text="У вас пока нет профиля. Создайте его, нажав на кнопку ниже.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Создать профиль 📝"),
                    ]
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
        return

    await message.answer(
        text=f"👤 Ваш профиль:\nИмя: {user.name}\nТелефон: {user.phone_number}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Изменить профиль", callback_data=f"edit_user:{user.id}"
                    ),
                ]
            ],
            resize_keyboard=True,
        ),
    )
