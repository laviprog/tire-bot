from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from src.users import UserService

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, text: str | None = None):
    await message.answer(
        text=f"Привет путник!\nЯ помогу тебе починить твой мот!" if not text else text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Кнопка 1"),
                    KeyboardButton(text="Кнопка 2"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
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
        "/garage - показать информацию о твоих мотоциклах\n"
    )


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
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Изменить профиль"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(Command("garage"))
async def garage_command(message: Message):
    await message.answer("Скоро будет!")
