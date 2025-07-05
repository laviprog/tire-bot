import re

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup


def is_valid_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    """
    return re.fullmatch(r"\+?[1-9]\d{9,14}$", phone) is not None


async def send_application(
    bot: Bot,
    chat_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    photo_id: str | None = None,
    video_id: str | None = None,
):
    if photo_id:
        await bot.send_photo(
            chat_id=chat_id, photo=photo_id, caption=text, reply_markup=reply_markup
        )
    elif video_id:
        await bot.send_video(
            chat_id=chat_id,
            video=video_id,
            caption=text,
            reply_markup=reply_markup,
        )
    else:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
