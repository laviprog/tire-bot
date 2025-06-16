from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.motorcycles import MotorcycleService, MotorcycleModel

router = Router()


@router.message(F.text == "Мой гараж 🏍️")
async def garage_command(message: Message):
    await message.answer(
        text="Добро пожаловать в ваш гараж! Здесь вы можете управлять своими мотоциклами.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Посмотреть мотоциклы 🏍️"),
                    KeyboardButton(text="Добавить мотоцикл ➕"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ],
            ],
            resize_keyboard=True,
        ),
    )


@router.message(F.text == "Посмотреть мотоциклы 🏍️")
async def view_motorcycles(message: Message, motorcycle_service: MotorcycleService):
    telegram_id = str(message.from_user.id)

    motorcycles = await motorcycle_service.list(MotorcycleModel.user_telegram_id == telegram_id)

    if not motorcycles:
        await message.answer(
            text="Упсс, у вас пока что нет мотоциклов. Самое время добавить новый мотоцикл!",
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
