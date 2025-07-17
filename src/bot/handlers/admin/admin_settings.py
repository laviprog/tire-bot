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
)

router = Router()


class AdminSettings(StatesGroup):
    max_records = State()
    operating_mode = State()
    excluded_dates = State()


@router.message(Text(SETTINGS), IsAdmin())
async def admin_settings(message: Message, messages: dict, keyboards: dict):
    await message.answer(
        text=messages["admin_settings_menu"],
        reply_markup=keyboards["admin_settings_menu"],
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
