from aiogram import Router
from aiogram.types import CallbackQuery

from src import log
from src.promo_codes import PromoCodeService

router = Router()


@router.callback_query(lambda callback_name: callback_name.data.startswith("delete_promo_code:"))
async def delete_motorcycle_callback(callback: CallbackQuery, promo_code_service: PromoCodeService):
    promo_code_id = callback.data.split(":")[1]

    try:
        await promo_code_service.delete(promo_code_id)
    except Exception as e:
        await callback.answer(
            text="К сожалению, не получилось удалить проомокод, попробуйте позже.", show_alert=True
        )
        log.error(f"Ошибка при удалении мотоцикла с ID {promo_code_id}: {e}")
        return
    await callback.message.delete()
    await callback.answer(text="Промокод успешно удален!", show_alert=True)
