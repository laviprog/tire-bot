from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

WORKER_KEYBOARDS = {
    "ru": {
        "worker_main_menu": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Пока ничего нет"),
                ],
            ],
            resize_keyboard=True,
        ),
    },
    # "en": {...},
}
