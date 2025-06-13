from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from src import log
from src.motorcycles import MotorcycleModel, MotorcycleService

router = Router()


class MotorcycleRegistration(StatesGroup):
    name = State()
    brand = State()
    motorcycle_model = State()
    engine = State()
    year = State()


@router.message(F.text == "Добавить мотоцикл 🏍️")
async def start_register_motorcycle(message: Message, state: FSMContext):
    await message.answer(
        text="Супер! Давай начнем регистрацию твоего мотоцикла.\nНапиши мне его имя (например, Мустанг)",
        reply_markup=None,
    )

    await state.set_state(MotorcycleRegistration.name)


@router.message(StateFilter(MotorcycleRegistration.name))
async def motorcycle_name_process(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)

    await message.answer(
        text="Классное имя! Теперь напиши марку мотоцикла (например, Harley-Davidson)",
        reply_markup=None,
    )

    await state.set_state(MotorcycleRegistration.brand)


@router.message(StateFilter(MotorcycleRegistration.brand))
async def motorcycle_brand_process(message: Message, state: FSMContext):
    brand = message.text.strip()
    await state.update_data(brand=brand)

    await message.answer(
        text="Отлично! Теперь напиши модель мотоцикла (например, Sportster)", reply_markup=None
    )

    await state.set_state(MotorcycleRegistration.motorcycle_model)


@router.message(StateFilter(MotorcycleRegistration.motorcycle_model))
async def motorcycle_model_process(message: Message, state: FSMContext):
    model = message.text.strip()
    await state.update_data(motorcycle_model=model)

    await message.answer(
        text="Хорошо! Теперь напиши тип двигателя (например, V-twin)", reply_markup=None
    )

    await state.set_state(MotorcycleRegistration.engine)


@router.message(StateFilter(MotorcycleRegistration.engine))
async def motorcycle_engine_process(message: Message, state: FSMContext):
    engine = message.text.strip()
    await state.update_data(engine=engine)

    await message.answer(
        text="Отлично! Теперь напиши год выпуска мотоцикла (например, 2020)", reply_markup=None
    )

    await state.set_state(MotorcycleRegistration.year)


@router.message(StateFilter(MotorcycleRegistration.year))
async def motorcycle_year_process(
    message: Message, state: FSMContext, motorcycle_service: MotorcycleService
):
    try:
        year = int(message.text.strip())
    except ValueError:
        await message.answer(
            text="Пожалуйста, введи корректный год выпуска (например, 2020).", reply_markup=None
        )
        return

    if year < 1930 or year > 2025:
        await message.answer(
            text="Пожалуйста, убедись, что ты ввел корректный год выпуска (например, 2020).",
            reply_markup=None,
        )
        return

    data = await state.get_data()

    motorcycle = MotorcycleModel(
        user_telegram_id=str(message.from_user.id),
        name=data["name"],
        brand=data["brand"],
        motorcycle_model=data["motorcycle_model"],
        engine=data["engine"],
        year=year,
    )
    try:
        await motorcycle_service.create(motorcycle)
    except Exception as error:
        await message.answer(
            text="Произошла ошибка при создании мотоцикла, пожалуйста, попробуйте позже",
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
        log.error(f"Ошибка при создании мотоцикла: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text="Твой мотоцикл успешно зарегистрирован! Ты можешь увидеть его в своем гараже.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Мой гараж 🏍️"),
                    KeyboardButton(text="Вернуться в начало ⬅️"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )
