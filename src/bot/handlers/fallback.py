from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router()


@router.message(StateFilter(None), ~F.text.startswith("/"))
async def fallback_message(message: Message, user_messages: dict):
    await message.answer(user_messages["fallback_message"])
