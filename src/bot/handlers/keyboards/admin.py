from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ADMIN_KEYBOARDS = {
    "ru": {
        "admin_main_menu": ReplyKeyboardMarkup(
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
    },
    # "en": {...},
}
