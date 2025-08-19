import json
from uuid import UUID

from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

from src import log
from src.applications import ApplicationService
from src.bot.utils import send_application
from src.motorcycles import MotorcycleService
from src.promo_codes import PromoCodeService
from src.users import UserService

router = Router()


@router.callback_query(lambda callback_name: callback_name.data.startswith("cancel_application:"))
async def cancel_application_callback(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    bot: Bot,
    user_service: UserService,
    motorcycle_service: MotorcycleService,
    promo_code_service: PromoCodeService,
    redis: Redis,
):
    application_id = callback.data.split(":")[1]
    try:
        application = await application_service.cancel(application_id)
        admins = await user_service.get_admins()
        user = await user_service.get_by_telegram_id(application.user_telegram_id)
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        promo_code = (
            await promo_code_service.get(application.promo_code_id)
            if application.promo_code_id
            else None
        )
    except Exception as e:
        await callback.answer(text=messages["cancel_application_error"], show_alert=True)
        log.error(f"Ошибка при отмене заявки с ID {application_id}: {e}")
        return
    await callback.message.delete()
    await callback.answer(text=messages["cancel_application_successful"], show_alert=True)

    data = await redis.get(str(application_id))
    data = json.loads(data) if data else {"admins": [], "user": {}, "worker": {}}
    try:
        for admin in data["admins"]:
            await bot.delete_message(
                int(admin["chat_id"]),
                int(admin["message_id"]),
            )
    except Exception as e:
        log.error(f"Ошибка при удалении сообщения администратора: {e}")

    for admin in admins:
        await send_application(
            bot,
            int(admin.telegram_id),
            text=messages["application_user_cancelled_notification_for_admin"](
                application, user, motorcycle, promo_code
            ),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )
    await redis.delete(str(application_id))


@router.callback_query(lambda callback_name: callback_name.data.startswith("admin_cancel_app:"))
async def admin_cancel_application_callback(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    bot: Bot,
    user_service: UserService,
    motorcycle_service: MotorcycleService,
    promo_code_service: PromoCodeService,
    redis: Redis,
):
    application_id = callback.data.split(":")[1]
    try:
        application = await application_service.cancel(UUID(application_id))
        user = await user_service.get_by_telegram_id(application.user_telegram_id)
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        promo_code = (
            await promo_code_service.get(application.promo_code_id)
            if application.promo_code_id
            else None
        )
    except Exception as e:
        await callback.answer(text=messages["cancel_application_error"], show_alert=True)
        log.error(f"Ошибка при отмене заявки с ID {application_id}: {e}")
        return

    data = await redis.get(str(application_id))
    data = json.loads(data) if data else {"admins": [], "user": {}, "worker": {}}
    try:
        await bot.delete_message(
            int(data["user"]["chat_id"]),
            int(data["user"]["message_id"]),
        )
        admins = data["admins"]
        for admin in admins:
            await bot.delete_message(
                int(admin["chat_id"]),
                int(admin["message_id"]),
            )
        if "worker" in data:
            await bot.delete_message(
                int(data["worker"]["chat_id"]),
                int(data["worker"]["message_id"]),
            )
    except Exception as e:
        log.error(f"Ошибка при удалении предыдущих сообщений: {e}")

    await callback.answer(text=messages["cancel_application_successful"], show_alert=True)

    if application.worker_telegram_id:
        await send_application(
            bot=bot,
            chat_id=int(application.worker_telegram_id),
            text=messages["application_cancelled_notification_for_worker"](
                application, user, motorcycle, promo_code
            ),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )

    await send_application(
        bot=bot,
        chat_id=int(application.user_telegram_id),
        text=messages["application_cancelled_notification_for_user"](
            application, motorcycle, promo_code
        ),
        photo_id=application.photo_id,
        video_id=application.video_id,
    )

    await redis.delete(str(application_id))


@router.callback_query(
    lambda callback_name: callback_name.data.startswith("admin_cancel_evacuation:")
)
async def admin_cancel_evacuation_callback(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    bot: Bot,
    redis: Redis,
):
    application_id = callback.data.split(":")[1]
    try:
        application = await application_service.cancel(UUID(application_id))
    except Exception as e:
        await callback.answer(text=messages["cancel_application_error"], show_alert=True)
        log.error(f"Ошибка при отмене заявки с ID {application_id}: {e}")
        return

    data = await redis.get(str(application_id))
    data = json.loads(data) if data else {"admins": [], "user": {}, "worker": {}}
    try:
        for admin in data["admins"]:
            await bot.delete_message(
                int(admin["chat_id"]),
                int(admin["message_id"]),
            )
        await bot.delete_message(
            int(data["user"]["chat_id"]),
            int(data["user"]["message_id"]),
        )
    except Exception as e:
        log.error(f"Ошибка при удалении предыдущих сообщений: {e}")

    await callback.answer(text=messages["cancel_application_successful"], show_alert=True)

    await bot.send_message(
        chat_id=application.user_telegram_id, text=messages["evacuation_cancel_admin"]
    )

    await redis.delete(str(application_id))


@router.callback_query(lambda callback_name: callback_name.data.startswith("cancel_evacuation:"))
async def cancel_evacuation_callback(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    bot: Bot,
    user_service: UserService,
    motorcycle_service: MotorcycleService,
    redis: Redis,
):
    application_id = callback.data.split(":")[1]
    try:
        application = await application_service.cancel(UUID(application_id))
        admins = await user_service.get_admins()
        user = await user_service.get_by_telegram_id(application.user_telegram_id)
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
    except Exception as e:
        await callback.answer(text=messages["cancel_application_error"], show_alert=True)
        log.error(f"Ошибка при отмене заявки с ID {application_id}: {e}")
        return

    data = await redis.get(str(application_id))
    data = json.loads(data) if data else {"admins": [], "user": {}, "worker": {}}

    await callback.message.delete()
    await callback.answer(text=messages["cancel_application_successful"], show_alert=True)

    try:
        for admin in data["admins"]:
            await bot.delete_message(
                int(admin["chat_id"]),
                int(admin["message_id"]),
            )
    except Exception as e:
        log.error(f"Ошибка при отмене заявки с ID {application_id}: {e}")

    for admin in admins:
        await bot.send_message(
            chat_id=admin.telegram_id,
            text=messages["evacuation_cancel_notification_for_admin"](
                application, user, motorcycle
            ),
        )

    await redis.delete(str(application_id))
