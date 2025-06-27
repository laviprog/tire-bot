from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

PROFILES = ["Мой профиль 👤"]
BACK_TO_START = ["Вернуться в начало ⬅️"]
LEAVE_UNCHANGED = ["Оставить без изменения"]
SKIP = ["Пропустить"]
ADD_MOTORCYCLE = ["Добавить мотоцикл ➕"]
CREATE_APPLICATION_SERVICE = ["Записаться в сервис 🛠️"]
CHECK_MOTORCYCLE = ["Посмотреть мотоциклы 🏍️"]
GARAGE = ["Мой гараж 🏍️"]

KEYBOARDS = {
    "ru": {
        "user_main_menu": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Вызвать эвакуатор 🚑"),
                    KeyboardButton(text="Записаться в сервис 🛠️"),
                ],
                [
                    KeyboardButton(text="Мой гараж 🏍️"),
                    KeyboardButton(text="Мой профиль 👤"),
                ],
            ],
            resize_keyboard=True,
        ),
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
        "worker_main_menu": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Пока ничего нет"),
                ],
            ],
            resize_keyboard=True,
        ),
        "profile": lambda user_id: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Изменить профиль", callback_data=f"edit_user:{user_id}"
                    ),
                ]
            ],
            resize_keyboard=True,
        ),
        "motorcycle": lambda motorcycle_id: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Изменить", callback_data=f"edit_motorcycle:{motorcycle_id}"
                    ),
                    InlineKeyboardButton(
                        text="Удалить", callback_data=f"delete_motorcycle:{motorcycle_id}"
                    ),
                ]
            ],
            resize_keyboard=True,
        ),
        "request_contact": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Отправить номер телефона", request_contact=True),
                ]
            ],
            resize_keyboard=True,
        ),
        "leave_unchanged": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
        "skip_step": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Пропустить"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
        "leave_unchanged_with_request_contact": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Отправить номер телефона", request_contact=True),
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
        "garage": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Посмотреть мотоциклы 🏍️"),
                    KeyboardButton(text="Добавить мотоцикл ➕"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ],
            ],
            resize_keyboard=True,
        ),
    },
    # "en": {...},
}
