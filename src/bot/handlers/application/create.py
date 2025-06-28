from datetime import datetime, timedelta, timezone
from uuid import UUID

from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup, InputFile,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from babel.dates import format_date

from src import log
from src.applications import ApplicationService, ApplicationModel
from src.bot.filters import Text
from src.bot.handlers.back import back_to_start
from src.bot.handlers.keyboards import CREATE_APPLICATION_SERVICE, SKIP
from src.bot.pagination import DatePagination
from src.bot.pagination.pagination import TimePagination
from src.motorcycles import MotorcycleModel, MotorcycleService
from src.promo_codes import PromoCodeService
from src.users import UserService

router = Router()


class ApplicationServiceCreate(StatesGroup):
    motorcycle_id = State()
    service_datetime = State()
    description = State()
    media_id = State()
    promo_code_id = State()


@router.message(Text(CREATE_APPLICATION_SERVICE))
async def start_create_application_service(
    message: Message,
    messages: dict,
    motorcycle_service: MotorcycleService,
):
    telegram_id = str(message.from_user.id)
    motorcycles = await motorcycle_service.list(MotorcycleModel.user_telegram_id == telegram_id)
    if not motorcycles:
        await message.answer(text=messages["no_motorcycles_for_application_service"])
        return

    builder = InlineKeyboardBuilder()

    for motorcycle in motorcycles:
        builder.row(
            InlineKeyboardButton(
                text=str(motorcycle.motorcycle_model),
                callback_data=f"motorcycle_for_application:{str(motorcycle.id)}",
            )
        )

    await message.answer(
        text=messages["choose_motorcycle_for_application_service"],
        reply_markup=builder.as_markup()
    )


@router.callback_query(
    lambda callback_name: callback_name.data.startswith(
        "motorcycle_for_application:"
    )
)
async def choose_motorcycle_process(
    callback: CallbackQuery, messages: dict, state: FSMContext, motorcycle_service: MotorcycleService
):
    motorcycle_id = callback.data.split(":")[1]
    motorcycle = await motorcycle_service.get(UUID(motorcycle_id))
    await state.update_data(motorcycle_id=motorcycle_id, motorcycle_model=motorcycle.motorcycle_model)
    await callback.message.edit_text(
        text=messages["choose_date_for_application_service"],
        reply_markup=await get_date_paginated_kb(datetime.today().replace(day=1)),
    )

async def get_time_slots(
    application_service: ApplicationService,
    day: int = 0,
    start_hours: int = 9,
    end_hours: int = 19,
    max_record: int = 10,
    interval_minutes: int = 30
) -> list[str]:
    start_day = datetime.today() + timedelta(days=day)
    start_day = start_day.replace(tzinfo=timezone.utc)
    end_day = start_day.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc)

    applications = await application_service.list(
        *[
            ApplicationModel.service_datetime >= start_day,
            ApplicationModel.service_datetime <= end_day
        ]
    )

    busy_time = {}

    for app in applications:
        time = app.service_datetime.strftime("%H-%M")
        busy_time[time] = busy_time.get(time, 0) + 1

    slots = []

    time = start_day.replace(hour=start_hours, minute=0, second=0, microsecond=0)
    while time.hour < end_hours:
        time_string = time.strftime("%H-%M")
        if busy_time.get(time_string, 0) < max_record:
            slots.append(time_string)
        time += timedelta(minutes=interval_minutes)

    return slots


async def get_date_paginated_kb(date: datetime) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    page_date = date.replace(day=1)
    today = date.today()

    formatted = format_date(page_date, format="LLL, yyyy", locale="ru")
    builder.row(
        InlineKeyboardButton(
            text="⬅️" if page_date.month > today.month else " ",
            callback_data=DatePagination(date=page_date.replace(month=page_date.month - 1).strftime("%m-%Y")).pack() if page_date.month > today.month else "skip_date",
        ),
        InlineKeyboardButton(
            text=formatted,
            callback_data="skip_date"
        ),
        InlineKeyboardButton(
            text="➡️",
            callback_data=DatePagination(date=page_date.replace(month=page_date.month + 1).strftime("%m-%Y")).pack(),
        ),
    )

    WEEKDAYS_SHORT_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    builder.row(*[InlineKeyboardButton(text=wd, callback_data='skip_date') for wd in WEEKDAYS_SHORT_RU])

    date = page_date
    buttons_row = []

    start_weekday = date.weekday()

    for _ in range(start_weekday):
        buttons_row.append(InlineKeyboardButton(text=" ", callback_data="skip_date"))

    while date.month == page_date.month:
        if date.date() < today.date():
            buttons_row.append(
                InlineKeyboardButton(
                    text=f"{date.day}",
                    callback_data='old_date',
                )
            )
        else:
            buttons_row.append(
                InlineKeyboardButton(
                    text=f"{date.day}",
                    callback_data=f"date_for_application:{date.strftime('%d-%m-%Y')}",
                )
            )

        if len(buttons_row) == 7:
            builder.row(*buttons_row)
            buttons_row = []

        date += timedelta(days=1)

    if buttons_row:
        while len(buttons_row) < 7:
            buttons_row.append(InlineKeyboardButton(text=" ", callback_data="skip_date"))
        builder.row(*buttons_row)

    return builder.as_markup()


async def get_time_paginated_kb(application_service: ApplicationService, date: datetime) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    day = date.day

    slots = await get_time_slots(application_service, day)

    builder.row(
        InlineKeyboardButton(
            text="⬅️" if day > 0 else " ",
            callback_data=TimePagination(date=(date - timedelta(days=1)).strftime("%d-%m-%Y")).pack() if day > 0 else "skip_date",
        ),
        InlineKeyboardButton(text=date.strftime("%d-%m-%Y"), callback_data="skip_date"),
        InlineKeyboardButton(
            text="➡️",
            callback_data=TimePagination(date=(date + timedelta(days=1)).strftime("%d-%m-%Y")).pack(),
        ),
    )
    buttons_row = []

    for i, slot in enumerate(slots):
        if i % 4 == 0 and i != 0:
            builder.row(*buttons_row)
            buttons_row = []
        buttons_row.append(InlineKeyboardButton(text=slot.replace('-', ':'), callback_data=f"time_for_application:{date.strftime('%d-%m-%Y') + ' ' + slot}"))

    if buttons_row:
        builder.row(*buttons_row)

    builder.row(
        InlineKeyboardButton(
            text="⬅️ Выбрать дату",
            callback_data=DatePagination(date=date.strftime("%m-%Y")).pack(),
        )
    )

    return builder.as_markup()


@router.callback_query(DatePagination.filter())
async def date_pagination_callback(callback: CallbackQuery, callback_data: DatePagination):
    date = callback_data.date

    await callback.message.edit_reply_markup(
        reply_markup=await get_date_paginated_kb(date=datetime.strptime(date, "%m-%Y"))
    )

@router.callback_query(TimePagination.filter())
async def time_pagination_callback(callback: CallbackQuery, callback_data: TimePagination, application_service: ApplicationService):
    date = datetime.strptime(callback_data.date, "%d-%m-%Y")

    await callback.message.edit_reply_markup(
        reply_markup=await get_time_paginated_kb(application_service, date=date)
    )


@router.callback_query(
    lambda callback_name: callback_name.data.startswith(
        "skip_date"
    )
)
async def skip_date(callback: CallbackQuery, messages: dict):
    await callback.answer(
        text=messages["skip_date"],
        show_alert=True
    )


@router.callback_query(
    lambda callback_name: callback_name.data.startswith(
        "old_date"
    )
)
async def old_date(callback: CallbackQuery, messages: dict):
    await callback.answer(
        text=messages["old_date"],
        show_alert=True
    )


@router.callback_query(
    lambda callback_name: callback_name.data.startswith(
        "date_for_application:"
    )
)
async def choose_date_process(
    callback: CallbackQuery, messages: dict, application_service: ApplicationService
):
    date = datetime.strptime(callback.data.split(":")[1], "%d-%m-%Y")
    await callback.message.edit_text(
        text=messages["choose_time_for_application_service"],
        reply_markup=await get_time_paginated_kb(application_service, date=date),
    )

@router.callback_query(
    lambda callback_name: callback_name.data.startswith(
        "time_for_application:"
    )
)
async def choose_time_process(
    callback: CallbackQuery, messages: dict, state: FSMContext
):
    selected_datetime = callback.data.split(":")[1]

    await state.update_data(datetime=selected_datetime)
    await state.set_state(ApplicationServiceCreate.description)
    await callback.message.delete()
    await callback.message.answer(
        text=messages["description_for_application_service"],
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(StateFilter(ApplicationServiceCreate.description))
async def description_process(
    message: Message,
    state: FSMContext,
    messages: dict,
    keyboards: dict,
):
    description = message.text.strip()

    await state.update_data(description=description)
    await state.set_state(ApplicationServiceCreate.media_id)
    await message.answer(
        text=messages["send_media_for_application_service"],
        reply_markup=keyboards["skip_step"],
    )

@router.message(StateFilter(ApplicationServiceCreate.media_id))
async def media_process(
    message: Message,
    state: FSMContext,
    messages: dict,
    keyboards: dict,
):
    if message.content_type == "text":
        if message.text.strip() in SKIP:
            await state.set_state(ApplicationServiceCreate.promo_code_id)
            await message.answer(text=messages["promo_code_for_application_service"], reply_markup=keyboards['skip_step'])
            return

    media_id = None
    if message.content_type == "photo":
        media_id = message.photo[-1].file_id
        await state.update_data(photo_id=media_id)
    elif message.content_type == "video":
        media_id = message.video.file_id
        await state.update_data(video_id=media_id)

    if not media_id:
        await message.answer(text=messages["media_for_application_service_not_valid"], reply_markup=keyboards['skip_step'])
        return

    await state.set_state(ApplicationServiceCreate.promo_code_id)
    await message.answer(text=messages["promo_code_for_application_service"], reply_markup=keyboards['skip_step'])


@router.message(StateFilter(ApplicationServiceCreate.promo_code_id))
async def promo_code_process(
    message: Message,
    state: FSMContext,
    promo_code_service: PromoCodeService,
    application_service: ApplicationService,
    user_service: UserService,
    messages: dict,
    keyboards: dict,
    bot: Bot
):
    promo_code = message.text.strip()
    if promo_code not in SKIP:
        if promo_code_id := await promo_code_service.check_code(promo_code):
            await state.update_data(promo_code_id=promo_code_id)
        else:
            await message.answer(text=messages["not_found_promo_code"], reply_markup=keyboards["skip_step"])
            return

    data = await state.get_data()
    service_dt = datetime.strptime(data.get("datetime"), "%d-%m-%Y %H-%M")
    service_dt = service_dt.replace(tzinfo=timezone.utc)
    application = ApplicationModel(
        user_telegram_id=str(message.from_user.id),
        motorcycle_id=data.get("motorcycle_id"),
        service_datetime=service_dt,
        description=data.get("description"),
        photo_id=data.get("photo_id", None),
        video_id=data.get("video_id", None),
        promo_code_id=data.get("promo_code_id", None),
    )

    try:
        application = await application_service.create(application)
    except Exception as error:
        await message.answer(
            text=messages["create_application_error"],
        )
        await back_to_start(message, user_service, messages, keyboards)
        log.error(f"Ошибка при создании заявки: {error}")
        return
    finally:
        await state.clear()

    if data.get("photo_id", None):
        await message.answer_photo(
            photo=data.get("photo_id"),
            caption=messages["application"](motorcycle_model=data.get("motorcycle_model"), description=data.get("description"), service_datetime=service_dt, status=application.status.value),
            reply_markup=keyboards["application"](application.id),
        )

    elif data.get("video_id", None):
        await message.answer_video(
            video=data.get("video_id"),
            caption=messages["application"](
                motorcycle_model=data.get("motorcycle_model"),
                description=data.get("description"),
                service_datetime=service_dt,
                status=application.status.value,
            ),
            reply_markup=keyboards["application"](application.id),
        )
    else:
        await message.answer(
            text=messages["application"](motorcycle_model=data.get("motorcycle_model"), description=data.get("description"), service_datetime=service_dt, status=application.status.value),
            reply_markup=keyboards["application"](application.id),
        )

    await back_to_start(message, user_service, messages, keyboards)
