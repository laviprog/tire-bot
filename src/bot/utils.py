import re

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message


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
) -> Message:
    if photo_id:
        return await bot.send_photo(
            chat_id=chat_id, photo=photo_id, caption=text, reply_markup=reply_markup
        )
    if video_id:
        return await bot.send_video(
            chat_id=chat_id,
            video=video_id,
            caption=text,
            reply_markup=reply_markup,
        )
    return await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


async def send_evacuation(
    bot: Bot,
    chat_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> Message:
    if latitude is not None and longitude is not None:
        message = await bot.send_location(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
        )
        return await bot.send_message(
            chat_id, text, reply_markup=reply_markup, reply_to_message_id=message.message_id
        )
    return await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
