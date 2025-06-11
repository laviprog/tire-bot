from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from src.bot.handlers.command import profile_command
from src.bot.utils import is_valid_phone_number
from src.users import UserService, UserModel

router = Router()


class UserInfo(StatesGroup):
    name = State()
    phone_number = State()


@router.message(F.text == "Создать профиль 📝")
async def create_profile_strart(message: Message, state: FSMContext, user_service: UserService):
    telegram_id = str(message.from_user.id)
    username = message.from_user.username

    if await user_service.get_by_telegram_id(telegram_id):
        await message.answer("Профиль уже существует.")
        return

    await user_service.create(
        UserModel(
            telegram_id=telegram_id,
            username=username,
        )
    )

    await state.set_state(UserInfo.name)
    await message.answer("Как вас зовут?")


@router.message(StateFilter(UserInfo.name))
async def process_name(message: Message, state: FSMContext, user_service: UserService):
    name = message.text
    telegram_id = str(message.from_user.id)

    user = await user_service.get_by_telegram_id(telegram_id)
    user.name = name
    await user_service.update(user)
    await state.set_state(UserInfo.phone_number)
    await message.answer(
        text="Поделитесь вашим номером телефона, нажав на кнопку ниже, или напишите его в обычном формате (например, 89017856745 или 79055943758)",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Отправить номер телефона", request_contact=True),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(StateFilter(UserInfo.phone_number))
async def process_phone_number(message: Message, state: FSMContext, user_service: UserService):
    phone_number = message.contact.phone_number if message.contact else message.text
    phone_number = phone_number.strip().replace(" ", "")

    if not is_valid_phone_number(phone_number):
        await message.answer("Пожалуйста, введите корректный номер телефона.")
        return

    telegram_id = str(message.from_user.id)

    user = await user_service.get_by_telegram_id(telegram_id)
    user.phone_number = phone_number
    await user_service.update(user)

    await state.clear()
    await profile_command(message, user_service, state)


class UserUpdate(StatesGroup):
    name = State()
    phone_number = State()


@router.message(F.text == "Изменить профиль")
async def edit_profile(message: Message, state: FSMContext, user_service: UserService):
    telegram_id = str(message.from_user.id)
    user = await user_service.get_by_telegram_id(telegram_id)

    if not user:
        await message.answer(
            text="У вас нет профиля. Создайте его, нажав на кнопку ниже.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Создать профиль 📝")]],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
        return

    await state.set_state(UserUpdate.name)
    await message.answer(
        text="Введите новое имя:",
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


@router.message(StateFilter(UserUpdate.name))
async def update_name(message: Message, state: FSMContext, user_service: UserService):
    if not message.text == "Оставить без изменения":
        new_name = message.text.strip()
        telegram_id = str(message.from_user.id)

        user = await user_service.get_by_telegram_id(telegram_id)
        user.name = new_name
        await user_service.update(user)

    await state.set_state(UserUpdate.phone_number)
    await message.answer(
        text="Введите новый номер телефона или нажмите кнопку ниже для отправки контакта",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Отправить номер телефона", request_contact=True),
                    KeyboardButton(text="Оставить без изменения"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(StateFilter(UserUpdate.phone_number))
async def update_phone_number(message: Message, state: FSMContext, user_service: UserService):
    if not message.text == "Оставить без изменения":
        if message.contact:
            phone_number = message.contact.phone_number
        else:
            phone_number = message.text.strip()

        telegram_id = str(message.from_user.id)
        user = await user_service.get_by_telegram_id(telegram_id)

        if not is_valid_phone_number(phone_number):
            await message.answer("Пожалуйста, введите корректный номер телефона.")
            return

        user.phone_number = phone_number
        await user_service.update(user)

    await state.clear()
    await profile_command(message, user_service)
