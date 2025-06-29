from aiogram import Router
from aiogram.types import CallbackQuery

from src import log
from src.applications import ApplicationService

router = Router()


@router.callback_query(lambda callback_name: callback_name.data.startswith("cancel_application:"))
async def cancel_application_callback(
    callback: CallbackQuery, application_service: ApplicationService, messages: dict
):
    application_id = callback.data.split(":")[1]
    try:
        await application_service.cancel(application_id)
    except Exception as e:
        await callback.answer(text=messages["cancel_application_error"], show_alert=True)
        log.error(f"Ошибка при отмене заявки с ID {application_id}: {e}")
        return
    await callback.message.delete()
    await callback.answer(text=messages["cancel_application_successful"], show_alert=True)
