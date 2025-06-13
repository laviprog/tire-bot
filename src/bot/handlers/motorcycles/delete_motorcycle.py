from aiogram import Router
from aiogram.types import CallbackQuery

from src import log
from src.motorcycles import MotorcycleService

router = Router()


@router.callback_query(lambda callback_name: callback_name.data.startswith("delete_motorcycle:"))
async def delete_motorcycle_callback(
    callback: CallbackQuery, motorcycle_service: MotorcycleService
):
    motorcycle_id = callback.data.split(":")[1]

    try:
        await motorcycle_service.delete(motorcycle_id)
    except Exception as e:
        await callback.answer(
            text="К сожалению, не получилось удалить мотоцикл, попробуйте позже.", show_alert=True
        )
        log.error(f"Ошибка при удалении мотоцикла с ID {motorcycle_id}: {e}")
        return
    await callback.message.delete()
    await callback.answer(text="Мотоцикл успещно удален!", show_alert=True)
