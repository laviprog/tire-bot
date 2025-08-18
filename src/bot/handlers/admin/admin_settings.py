import json
from datetime import datetime

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from redis.asyncio import Redis

from src.bot.filters import IsAdmin, Text
from src.bot.handlers.keyboards import (
    SETTINGS,
    MAX_RECORDS,
    OPERATING_MODE,
    EXCLUDED_DATES,
    LEAVE_UNCHANGED,
    CONTACT_INFORMATION,
    CHANGE_CONTACT_INFORMATION,
    ADMIN_CONTACTS_FOR_USER,
)

router = Router()


class AdminSettings(StatesGroup):
    max_records = State()
    operating_mode = State()
    excluded_dates = State()
    contact_phone = State()
    contact_username = State()
    contact_name = State()


@router.message(Text(SETTINGS), IsAdmin())
async def admin_settings(message: Message, messages: dict, keyboards: dict):
    await message.answer(
        text=messages["admin_settings_menu"],
        reply_markup=keyboards["admin_settings_menu"],
    )


@router.message(Text(ADMIN_CONTACTS_FOR_USER))
async def contacts(message: Message, redis: Redis, messages: dict):
    admin_contacts = await redis.get("contacts_information")
    if admin_contacts:
        admin_contacts = json.loads(admin_contacts.decode("utf-8"))
    # await message.answer(
    #     text=messages["admin_contacts_information"](admin_contacts),
    # )
    await message.answer_contact(
        admin_contacts["phone"],
        admin_contacts["name"],
    )
    await message.answer(
        text=messages["admin_tg"](admin_contacts["username"]),
    )


@router.message(Text(CONTACT_INFORMATION), IsAdmin())
async def admin_contact_information(
    message: Message, redis: Redis, messages: dict, keyboards: dict, state: FSMContext
):
    admin_contacts = await redis.get("contacts_information")
    if admin_contacts:
        admin_contacts = json.loads(admin_contacts)

    await message.answer(
        text=messages["admin_contacts_information"](admin_contacts),
        reply_markup=keyboards["admin_contact_information_menu"],
    )


@router.message(Text(CHANGE_CONTACT_INFORMATION), IsAdmin())
async def admin_change_contact_information(
    message: Message, state: FSMContext, messages: dict, keyboards: dict, redis: Redis
):
    admin_contacts = await redis.get("contacts_information")
    admin_contacts = json.loads(admin_contacts)
    phone = admin_contacts.get("phone", "+7 968 428-00-33")
    await state.update_data(
        phone=phone,
        username=admin_contacts.get("username", "@CyberMot_Top"),
        name=admin_contacts.get("name", "Иван"),
    )
    await state.set_state(AdminSettings.contact_phone)
    await message.answer(
        text=messages["admin_edit_phone_contact"](phone),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(AdminSettings.contact_phone), IsAdmin())
async def admin_change_phone_process(
    message: Message, messages: dict, keyboards: dict, state: FSMContext
):
    contact_phone = message.text.strip()
    name = await state.get_value("name", "Иван")

    if contact_phone not in LEAVE_UNCHANGED:
        await state.update_data(phone=contact_phone)

    await state.set_state(AdminSettings.contact_name)
    await message.answer(
        text=messages["admin_edit_name_contact"](name),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(AdminSettings.contact_name), IsAdmin())
async def admin_change_name_process(
    message: Message, messages: dict, keyboards: dict, state: FSMContext
):
    contact_name = message.text.strip()
    username = await state.get_value("username", "@CyberMot_Top")

    if contact_name not in LEAVE_UNCHANGED:
        await state.update_data(name=contact_name)

    await state.set_state(AdminSettings.contact_username)
    await message.answer(
        text=messages["admin_edit_username_contact"](username),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(AdminSettings.contact_username), IsAdmin())
async def admin_change_username_process(
    message: Message, messages: dict, keyboards: dict, redis: Redis, state: FSMContext
):
    contact_username = message.text.strip()

    if contact_username not in LEAVE_UNCHANGED:
        await state.update_data(username=contact_username)

    data = await state.get_data()
    admin_contacts = {
        "phone": data.get("phone", "+7 968 428-00-33"),
        "username": data.get("username", "@CyberMot_Top"),
        "name": data.get("name", "Иван"),
    }
    await redis.set("contacts_information", json.dumps(admin_contacts))

    await state.clear()
    await message.answer(
        text=messages["admin_contacts_information"](admin_contacts),
        reply_markup=keyboards["admin_main_menu"],
    )


@router.message(Text(MAX_RECORDS), IsAdmin())
async def admin_max_records(
    message: Message, state: FSMContext, messages: dict, keyboards: dict, redis: Redis
):
    max_records = await redis.get("max_records")
    if max_records:
        max_records = int(max_records.decode("utf-8"))

    await state.set_state(AdminSettings.max_records)
    await message.answer(
        text=messages["admin_max_records"](max_records),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(AdminSettings.max_records), IsAdmin())
async def admin_max_records_process(
    message: Message, messages: dict, keyboards: dict, redis: Redis, state: FSMContext
):
    max_records = message.text.strip()

    if max_records not in LEAVE_UNCHANGED:
        try:
            max_records = int(max_records)
            if max_records < 1:
                raise ValueError("Max records must be greater than 0.")
            await redis.set("max_records", max_records)
        except ValueError:
            await message.answer(text=messages["invalid_max_records"])
            return
    else:
        max_records = await redis.get("max_records")
        if max_records:
            max_records = int(max_records.decode("utf-8"))
        else:
            max_records = 10

    await state.clear()
    await message.answer(
        text=messages["admin_max_records_saved"](max_records),
        reply_markup=keyboards["admin_settings_menu"],
    )


@router.message(Text(OPERATING_MODE), IsAdmin())
async def admin_operating_mode(
    message: Message, state: FSMContext, messages: dict, keyboards: dict, redis: Redis
):
    operating_mode = await redis.get("operating_mode")
    if operating_mode:
        operating_mode = operating_mode.decode("utf-8")
    else:
        operating_mode = "10-20"

    await state.set_state(AdminSettings.operating_mode)
    await message.answer(
        text=messages["admin_operating_mode"](operating_mode),
        reply_markup=keyboards["leave_unchanged"],
    )


@router.message(StateFilter(AdminSettings.operating_mode), IsAdmin())
async def admin_operating_mode_process(
    message: Message, messages: dict, keyboards: dict, redis: Redis, state: FSMContext
):
    operating_mode = message.text.strip()

    if operating_mode not in LEAVE_UNCHANGED:
        try:
            start, end = map(int, [value.strip() for value in operating_mode.split("-")])
            if 0 < start < end:
                await redis.set("operating_mode", operating_mode)
            else:
                raise ValueError(
                    "Operating mode must be greater than or equal to 0. Also start < end!"
                )
        except Exception:
            await message.answer(text=messages["invalid_operating_mode"])
            return
    else:
        operating_mode = await redis.get("operating_mode")
        if operating_mode:
            operating_mode = operating_mode.decode("utf-8")
        else:
            operating_mode = "10-20"

    await state.clear()
    await message.answer(
        text=messages["admin_operating_mode_saved"](operating_mode),
        reply_markup=keyboards["admin_settings_menu"],
    )


@router.message(Text(EXCLUDED_DATES), IsAdmin())
async def admin_excluded_dates(message: Message, state: FSMContext, messages: dict):
    await state.set_state(AdminSettings.excluded_dates)
    await message.answer(
        text=messages["admin_excluded_dates"],
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(StateFilter(AdminSettings.excluded_dates), IsAdmin())
async def admin_exluded_dates_process(
    message: Message, messages: dict, keyboards: dict, redis: Redis, state: FSMContext
):
    excluded_dates_new = message.text.strip()

    if excluded_dates_new not in ["–", "-"]:
        try:
            excluded_dates_cleared = []
            excluded_dates = await redis.get("excluded_dates")
            if excluded_dates:
                excluded_dates = excluded_dates.decode("utf-8")
                excluded_dates = [
                    datetime.strptime(date.strip(), "%d.%m.%Y")
                    for date in excluded_dates.split(",")
                ]
                excluded_dates_cleared = [date for date in excluded_dates if date > datetime.now()]

            excluded_dates_list = [
                datetime.strptime(date.strip(), "%d.%m.%Y")
                for date in excluded_dates_new.split(",")
            ]
            excluded_dates_list = [date.strftime("%d.%m.%Y") for date in excluded_dates_list]
            for date in excluded_dates_cleared:
                if date not in excluded_dates_list:
                    excluded_dates_list.append(date.strftime("%d.%m.%Y"))

            await redis.set("excluded_dates", ",".join(excluded_dates_list))

            await state.clear()
            await message.answer(
                text=messages["admin_excluded_dates_saved"](excluded_dates_new),
                reply_markup=keyboards["admin_settings_menu"],
            )
        except Exception:
            await message.answer(text=messages["invalid_excluded_dates"])
            return
    elif excluded_dates_new in ["–", "-"]:
        await state.clear()
        await message.answer(
            text=messages["admin_excluded_dates_skipped"],
            reply_markup=keyboards["admin_settings_menu"],
        )
