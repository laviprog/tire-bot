from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router()


@router.message(StateFilter(None), ~F.text.startswith("/"))
async def fallback_message(message: Message, messages: dict):
    await message.answer(messages["fallback_message"])
