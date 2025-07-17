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
CREATE_APPLICATION_EVACUATION = ["Вызвать эвакуатор 🚑"]
CHECK_MOTORCYCLE = ["Посмотреть мотоциклы 🏍️"]
GARAGE = ["Мой гараж 🏍️"]
SETTINGS = ["Настройки ⚙️"]
MANAGE_ROLES = ["Управление ролями 👥"]
ADD_ADMIN = ["Добавить админа"]
ADD_WORKER = ["Добавить работника"]

MAX_RECORDS = ["Максимальное количество записей"]
OPERATING_MODE = ["Режим работы"]
EXCLUDED_DATES = ["Исключить рабочие дни"]
ADD_PROMO_CODE = ["Добавить промокод ➕"]
CHECK_PROMO_CODES = ["Посмотреть промокоды ✅"]
PROMO_CODES = ["Промокоды 💳"]

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
                    KeyboardButton(text="Управление ролями 👥"),
                ],
                [
                    KeyboardButton(text="Промокоды 💳"),
                    KeyboardButton(text="Настройки ⚙️"),
                ],
            ],
            resize_keyboard=True,
        ),
        "manage_roles_menu": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Добавить админа"),
                    KeyboardButton(text="Добавить работника"),
                ],
                [
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ],
            ],
            resize_keyboard=True,
        ),
        "admin_settings_menu": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Максимальное количество записей"),
                    KeyboardButton(text="Режим работы"),
                ],
                [
                    KeyboardButton(text="Исключить рабочие дни"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ],
            ]
        ),
        "worker_main_menu": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Мой профиль 👤"),
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
        "application": lambda application_id: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Отменить", callback_data=f"cancel_application:{application_id}"
                    ),
                ]
            ]
        ),
        "application_evacuation": lambda application_id: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Отменить", callback_data=f"cancel_evacuation:{application_id}"
                    ),
                ]
            ]
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
        "location_for_application_evacuation": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Отправить местоположение", request_location=True),
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
        "promo_codes_menu": ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Посмотреть промокоды ✅"),
                    KeyboardButton(text="Добавить промокод ➕"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ],
            ],
            resize_keyboard=True,
        ),
        "new_application_notification_for_admin": lambda application_number: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Назначить работника 👷",
                        callback_data=f"add_worker_to_app:{application_number}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Отклонить ❌",
                        callback_data=f"admin_cancel_app:{application_number}",
                    ),
                ],
            ],
            resize_keyboard=True,
        ),
        "new_evacuation_notification_for_admin": lambda application_number, application_id: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Взять в работу 🛠️",
                        callback_data=f"evacuation_in_progress:{application_number}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Отклонить ❌",
                        callback_data=f"admin_cancel_evacuation:{application_id}",
                    ),
                ],
            ],
            resize_keyboard=True,
        ),
        "admin_cancel_app": lambda application_number: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Отменить",
                        callback_data=f"admin_cancel_app:{application_number}",
                    ),
                ],
            ],
            resize_keyboard=True,
        ),
        "add_worker_to_app": lambda application_number, workers: InlineKeyboardMarkup(
            inline_keyboard=[
                *(
                    [
                        InlineKeyboardButton(
                            text=f"{worker.name} @{worker.username}",
                            callback_data=f"select_worker:{application_number}:{worker.username}",
                        )
                    ]
                    for worker in workers
                ),
                [
                    InlineKeyboardButton(
                        text="Назад ⬅️", callback_data=f"back_to_app_menu:{application_number}"
                    )
                ],
            ]
        ),
        "promo_code_options": lambda promo_code_id: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Изменить ✏️", callback_data=f"edit_promo_code:{promo_code_id}"
                    ),
                    InlineKeyboardButton(
                        text="Удалить ❌",
                        callback_data=f"delete_promo_code:{promo_code_id}",
                    ),
                ],
            ],
            resize_keyboard=True,
        ),
        "worker_in_progress": lambda application_number: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Начать работу 🛠️",
                        callback_data=f"in_progress_application:{application_number}",
                    ),
                ],
            ],
            resize_keyboard=True,
        ),
        "worker_completed": lambda application_number: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Закончить работу ✅",
                        callback_data=f"completed_application:{application_number}",
                    ),
                ],
            ],
            resize_keyboard=True,
        ),
        "evacuation_completed": lambda application_number: InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Закончить эвакуацию ✅",
                        callback_data=f"completed_evacuation:{application_number}",
                    ),
                ],
            ],
            resize_keyboard=True,
        ),
    },
    # "en": {...},
}
