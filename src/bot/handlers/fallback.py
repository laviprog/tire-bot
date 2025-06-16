from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router()


@router.message(StateFilter(None), ~F.text.startswith("/"))
async def fallback_message(message: Message):
    await message.answer(
        "Упс! Я не понимаю, что ты имеешь в виду. Пожалуйста, используй команды или напиши /help для получения помощи."
    )
