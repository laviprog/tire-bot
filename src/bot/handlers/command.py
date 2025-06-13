from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.motorcycles import MotorcycleService, MotorcycleModel
from src.users import UserService

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, text: str | None = None):
    await message.answer(
        text="Привет путник!\nЯ помогу тебе починить твой мот!" if not text else text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Мой гараж 🏍️"),
                    KeyboardButton(text="Мой профиль 👤"),
                ]
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
        "/garage - показать информацию о твоих мотоциклах\n"
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


@router.message(F.text == "Мой гараж 🏍️")
@router.message(Command("garage"))
async def garage_command(message: Message, motorcycle_service: MotorcycleService):
    telegram_id = str(message.from_user.id)

    motorcycles = await motorcycle_service.list(MotorcycleModel.user_telegram_id == telegram_id)

    if not motorcycles:
        await message.answer(
            text="Упсс, ваш гараж пуст. Самое время добавить мотоцикл!",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Добавить мотоцикл 🏍️"),
                        KeyboardButton(text="Вернуться в начало ⬅️"),
                    ]
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
        return

    for motorcycle in motorcycles:
        await message.answer(
            text=(
                f"🏍️ Мотоцикл:\n"
                f"Имя: {motorcycle.name}\n"
                f"Марка: {motorcycle.brand}\n"
                f"Модель: {motorcycle.motorcycle_model}\n"
                f"Движок: {motorcycle.engine}\n"
                f"Год выпуска: {motorcycle.year}\n"
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Изменить", callback_data=f"edit_motorcycle:{motorcycle.id}"
                        ),
                        InlineKeyboardButton(
                            text="Удалить", callback_data=f"delete_motorcycle:{motorcycle.id}"
                        ),
                    ]
                ],
                resize_keyboard=True,
            ),
        )
