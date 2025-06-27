from datetime import datetime, timedelta, timezone

from advanced_alchemy.types import DateTimeUTC
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src import log
from src.applications import ApplicationService, ApplicationModel
from src.bot.filters import Text
from src.bot.handlers.back import back_to_start
from src.bot.handlers.keyboards import CREATE_APPLICATION_SERVICE, SKIP
from src.bot.pagination import DatePagination
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
    callback: CallbackQuery, application_service: ApplicationService, messages: dict, state: FSMContext
):
    motorcycle_id = callback.data.split(":")[1]

    await state.update_data(motorcycle_id=motorcycle_id)
    await callback.message.edit_text(
        text=messages["choose_datetime_for_application_service"],
        reply_markup=await get_date_paginated_kb(application_service),
    )

async def get_time_slots(
    application_service: ApplicationService,
    day: int = 0,
) -> list[tuple[tuple[str, str], datetime]]:
    start_day = datetime.today() + timedelta(days=day)
    end_day = start_day.replace(hour=23, minute=59, second=59, microsecond=999999)

    # applications = await application_service.list(
    #     ApplicationModel.service_datetime.between(start_day, end_day)
    # )
    #
    # busy_hours = [app.service_datetime.time().hour for app in applications]
    busy_hours = []


    free_slots = [
        ((f"{hour}:00", f"{hour + 1}:00"), start_day.replace(hour=hour)) for hour in range(9, 21) if hour not in busy_hours
    ]

    return free_slots


async def get_date_paginated_kb(application_service: ApplicationService, day: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    slots = await get_time_slots(application_service, day)
    slots_composed = [f"{slot[0][0]} - {slot[0][1]}" for slot in slots]
    page_date = datetime.today() + timedelta(days=day)
    builder.row(InlineKeyboardButton(text=page_date.strftime("%d-%m-%Y"), callback_data="skip_date"))
    buttons_row = []

    for i, slot in enumerate(slots_composed):
        if i % 2 == 0 and i != 0:
            builder.row(*buttons_row)
            buttons_row = []
        buttons_row.append(InlineKeyboardButton(text=slot, callback_data=f"datetime_for_application:{slots[i][1].isoformat()}"))

    if buttons_row:
        builder.row(*buttons_row)

    buttons_row = []
    if day > 0:
        buttons_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=DatePagination(day=day - 1).pack(),
            )
        )
    buttons_row.append(
        InlineKeyboardButton(
            text="➡️",
            callback_data=DatePagination(day=day + 1).pack(),
        )
    )
    builder.row(*buttons_row)

    return builder.as_markup()


@router.callback_query(DatePagination.filter())
async def pagination_callback(callback: CallbackQuery, callback_data: DatePagination, application_service: ApplicationService):
    day = callback_data.day

    await callback.message.edit_reply_markup(
        reply_markup=await get_date_paginated_kb(application_service, day=day)
    )

@router.callback_query(
    lambda callback_name: callback_name.data.startswith(
        "skip_date"
    )
)
async def skip_date(callback: CallbackQuery):
    await callback.answer(
        text="Выберите конкретное время",
        show_alert=True
    )

@router.callback_query(
    lambda callback_name: callback_name.data.startswith(
        "datetime_for_application:"
    )
)
async def choose_datetime_process(
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
):
    promo_code = message.text.strip()
    if promo_code not in SKIP:
        if promo_code_id := await promo_code_service.check_code(promo_code):
            await state.update_data(promo_code_id=promo_code_id)
        else:
            await message.answer(text=messages["not_found_promo_code"], reply_markup=keyboards["skip_step"])
            return

    data = await state.get_data()
    service_dt = datetime.fromisoformat(data.get("datetime"))
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

    # await message.answer(
    #     text=messages["motorcycle"](motorcycle_model, year),
    #     reply_markup=keyboards["motorcycle"](motorcycle.id),
    # )

    await message.answer(
        "Заявка успешно создана"
    )

    await back_to_start(message, user_service, messages, keyboards)
