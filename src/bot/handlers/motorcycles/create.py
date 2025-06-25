from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from src import log
from src.bot.handlers.back import back_to_start
from src.bot.handlers.keyboards.utils import ADD_MOTORCYCLE
from src.motorcycles import MotorcycleModel, MotorcycleService
from src.users import UserService

router = Router()


class MotorcycleCreate(StatesGroup):
    motorcycle_model = State()
    year = State()


@router.message(*[F.text == text for text in ADD_MOTORCYCLE])
async def start_create_motorcycle(message: Message, state: FSMContext, user_messages: dict):
    await message.answer(
        text=user_messages["add_motorcycle_model_process"],
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(MotorcycleCreate.motorcycle_model)


@router.message(StateFilter(MotorcycleCreate.motorcycle_model))
async def motorcycle_model_process(message: Message, state: FSMContext, user_messages: dict):
    model = message.text.strip()
    await state.update_data(motorcycle_model=model)

    await message.answer(text=user_messages["add_motorcycle_year_process"])

    await state.set_state(MotorcycleCreate.year)


@router.message(StateFilter(MotorcycleCreate.year))
async def motorcycle_year_process(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    motorcycle_service: MotorcycleService,
    user_messages: dict,
    user_keyboards: dict,
    admin_keyboards: dict,
    worker_keyboards: dict,
):
    try:
        year = int(message.text.strip())
    except ValueError:
        await message.answer(text=user_messages["not_valid_year"])
        return

    if year < 1930 or year > 2025:
        await message.answer(
            text=user_messages["not_valid_year"],
        )
        return

    data = await state.get_data()

    motorcycle_model = data["motorcycle_model"]

    motorcycle = MotorcycleModel(
        user_telegram_id=str(message.from_user.id),
        motorcycle_model=motorcycle_model,
        year=year,
    )
    try:
        motorcycle = await motorcycle_service.create(motorcycle)
    except Exception as error:
        await message.answer(
            text=user_messages["add_motorcycle_error"],
        )
        await back_to_start()
        log.error(f"Ошибка при создании мотоцикла: {error}")
        return
    finally:
        await state.clear()

    await message.answer(
        text=user_messages["motorcycle"](motorcycle_model, year),
        reply_markup=user_keyboards["motorcycle"](motorcycle.id),
    )

    await back_to_start(
        message, user_service, user_messages, user_keyboards, admin_keyboards, worker_keyboards
    )
