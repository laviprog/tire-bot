from aiogram import Router, Bot
from aiogram.types import CallbackQuery

from src import log
from src.applications import ApplicationService, Status
from src.bot.utils import send_application
from src.motorcycles import MotorcycleService
from src.promo_codes import PromoCodeService
from src.users import UserService

router = Router()


@router.callback_query(lambda callback_name: callback_name.data.startswith("add_worker_to_app:"))
async def admin_choosing_worker(
    callback: CallbackQuery, user_service: UserService, keyboards: dict
):
    application_number = callback.data.split(":")[1]
    try:
        workers = await user_service.get_workers()
    except Exception:
        await callback.answer(
            text="Ошибка при получении списка работников. Попробуйте позже.", show_alert=True
        )
        return

    await callback.message.edit_reply_markup(
        reply_markup=keyboards["add_worker_to_app"](application_number, workers)
    )


@router.callback_query(lambda callback_name: callback_name.data.startswith("back_to_app_menu:"))
async def back_to_app_menu(callback: CallbackQuery, keyboards: dict):
    application_number = callback.data.split(":")[1]
    await callback.message.edit_reply_markup(
        reply_markup=keyboards["new_application_notification_for_admin"](application_number)
    )


@router.callback_query(lambda callback_name: callback_name.data.startswith("select_worker:"))
async def admin_assigned_worker(
    callback: CallbackQuery,
    user_service: UserService,
    application_service: ApplicationService,
    keyboards: dict,
    messages: dict,
    promo_code_service: PromoCodeService,
    motorcycle_service: MotorcycleService,
    bot: Bot,
):
    application_number = int(callback.data.split(":")[1])
    worker_username = callback.data.split(":")[2]

    try:
        worker = await user_service.get_by_username(worker_username)
        if not worker:
            await callback.answer(text=messages["worker_not_found"], show_alert=True)
            return
        application = await application_service.get_by_number(application_number)
        if not application:
            await callback.answer(text=messages["application_not_found"], show_alert=True)
            return
        user = await user_service.get_by_telegram_id(application.user_telegram_id)
        if not user:
            raise ValueError(f"User with telegram ID {application.user_telegram_id} not found")
        promo_code = (
            await promo_code_service.get(application.promo_code_id)
            if application.promo_code_id
            else None
        )
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        application.status = Status.ASSIGNED
        application.worker_telegram_id = worker.telegram_id
        application = await application_service.update(application)
        await callback.message.delete()
        await send_application(
            bot,
            callback.message.chat.id,
            text=messages["assigned_application_notification_for_admin"](
                application, user, motorcycle, promo_code, worker
            ),
            reply_markup=keyboards["admin_cancel_app"](application_number),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )
        await send_application(
            bot,
            int(worker.chat_id),
            text=messages["assigned_application_notification_for_worker"](
                application, user, motorcycle, promo_code
            ),
            reply_markup=keyboards["worker_in_progress"](application_number),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )
        await send_application(
            bot,
            int(user.telegram_id),
            text=messages["assigned_application_notification_for_user"](
                application, motorcycle, promo_code
            ),
            reply_markup=keyboards["application"](application.id),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )

    except Exception as e:
        await callback.answer(text=messages["assign_application_error"], show_alert=True)
        log.error(
            f"Ошибка при назначении работника на заказ. Application: {application_number}, Worker username: {worker_username}. Error: {e}"
        )
        return
