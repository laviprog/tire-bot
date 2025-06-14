from uuid import UUID

from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton

from src import log
from src.motorcycles import MotorcycleService

router = Router()


class MotorcycleUpdate(StatesGroup):
    name = State()
    brand = State()
    motorcycle_model = State()
    engine = State()
    year = State()


@router.callback_query(lambda callback_name: callback_name.data.startswith("edit_motorcycle:"))
async def edit_motorcycle_callback(
    callback: CallbackQuery, bot: Bot, state: FSMContext, motorcycle_service: MotorcycleService
):
    motorcycle_id = callback.data.split(":")[1]

    try:
        motorcycle = await motorcycle_service.get(motorcycle_id)
    except Exception as e:
        await callback.answer(
            text="К сожалению, не удалось найти мотоцикл. Попробуйте позже.", show_alert=True
        )
        log.error(f"Ошибка при получении мотоцикла с ID {motorcycle_id}: {e}")
        return

    await state.update_data(
        id=str(motorcycle.id),
        name=motorcycle.name,
        brand=motorcycle.brand,
        motorcycle_model=motorcycle.motorcycle_model,
        engine=motorcycle.engine,
        year=motorcycle.year,
    )
    await state.set_state(MotorcycleUpdate.name)
    await callback.message.delete()
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=f"Текущее имя мотоцикла: {motorcycle.name}\nНапиши новое имя мотоцикла (например, Мой любимый мотоцикл) или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(MotorcycleUpdate.name))
async def motorcycle_update_name_process(message: Message, state: FSMContext):
    name = message.text.strip()

    if not name == "Оставить без изменения":
        await state.update_data(name=name)

    data = await state.get_data()
    motorcycle_brand = data["brand"]

    await state.set_state(MotorcycleUpdate.brand)

    await message.answer(
        text=f"Текущая марка: {motorcycle_brand}\nНапиши новую марку мотоцикла (например, Harley-Davidson) или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(MotorcycleUpdate.brand))
async def motorcycle_update_brand_process(message: Message, state: FSMContext):
    brand = message.text.strip()

    if not brand == "Оставить без изменения":
        await state.update_data(brand=brand)

    data = await state.get_data()
    motorcycle_model = data["motorcycle_model"]

    await state.set_state(MotorcycleUpdate.motorcycle_model)
    await message.answer(
        text=f"Текущая модель: {motorcycle_model}\nНапиши новую модель мотоцикла (например, Sportster) или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(MotorcycleUpdate.motorcycle_model))
async def motorcycle_update_model_process(message: Message, state: FSMContext):
    model = message.text.strip()

    if not model == "Оставить без изменения":
        await state.update_data(motorcycle_model=model)

    data = await state.get_data()
    motorcycle_engine = data["engine"]

    await state.set_state(MotorcycleUpdate.engine)
    await message.answer(
        text=f"Текущий движок: {motorcycle_engine}\nНапиши новый движок мотоцикла (например, V-twin) или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )


@router.message(StateFilter(MotorcycleUpdate.engine))
async def motorcycle_update_engine_process(message: Message, state: FSMContext):
    engine = message.text.strip()
    if not engine == "Оставить без изменения":
        await state.update_data(engine=engine)

    data = await state.get_data()
    motorcycle_year = data["year"]

    await state.set_state(MotorcycleUpdate.year)
    await message.answer(
        text=f"Текущий год выпуска: {motorcycle_year}\nНапиши новый год выпуска мотоцикла (например, 2020) или оставь без изменений, нажав на кнопку ниже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(StateFilter(MotorcycleUpdate.year))
async def motorcycle_update_year_process(
    message: Message, state: FSMContext, motorcycle_service: MotorcycleService
):
    year = message.text.strip()

    if not year == "Оставить без изменения":
        try:
            year = int(message.text.strip())
        except ValueError:
            await message.answer(
                text="Пожалуйста, введи корректный год выпуска (например, 2020).",
            )
            return

        if year < 1930 or year > 2025:
            await message.answer(
                text="Пожалуйста, убедись, что ты ввел корректный год выпуска (например, 2020).",
            )
            return

        await state.update_data(year=year)

    data = await state.get_data()

    try:
        await motorcycle_service.update(
            data={
                "name": data["name"],
                "brand": data["brand"],
                "motorcycle_model": data["motorcycle_model"],
                "engine": data["engine"],
                "year": data["year"],
            },
            item_id=UUID(data["id"]),
        )
    except Exception as error:
        await message.answer(
            text="Произошла ошибка при обновлении мотоцикла, пожалуйста, попробуйте позже",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Вернуться в начало ⬅️"),
                    ]
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
        log.error(f"Ошибка при обновлении мотоцикла: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text="Твой мотоцикл успешно обновлен! Ты можешь увидеть его в своем гараже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Мой гараж 🏍️"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ]
            ],
            resize_keyboard=True,
        ),
    )
