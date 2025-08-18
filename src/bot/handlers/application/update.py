import json

from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from redis.asyncio import Redis

from src import log
from src.applications import ApplicationService, Status
from src.bot.utils import send_application
from src.motorcycles import MotorcycleService
from src.promo_codes import PromoCodeService
from src.users import UserService

router = Router()


@router.callback_query(
    lambda callback_name: callback_name.data.startswith("in_progress_application:")
)
async def change_status_in_progress_application_callback(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    keyboards: dict,
    bot: Bot,
    motorcycle_service: MotorcycleService,
    promo_code_service: PromoCodeService,
    user_service: UserService,
    redis: Redis,
):
    application_number = int(callback.data.split(":")[1])
    try:
        application = await application_service.get_by_number(application_number)
        if not application:
            raise ValueError(f"Application with number {application_number} not found")
        user = await user_service.get_by_telegram_id(str(application.user_telegram_id))
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        promo_code = (
            await promo_code_service.get(application.promo_code_id)
            if application.promo_code_id
            else None
        )
        admins = await user_service.get_admins()
        await application_service.update({"status": Status.IN_PROGRESS}, application.id)
        await callback.message.delete()
        data = await redis.get(str(application.id))
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
            log.error(f"Error deleting messages: {e}")

        worker_message = await send_application(
            bot,
            callback.message.chat.id,
            text=messages["assigned_application_notification_for_worker"](
                application, user, motorcycle, promo_code
            ),
            reply_markup=keyboards["worker_completed"](application_number),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )
        data["worker"] = {
            "chat_id": worker_message.chat.id,
            "message_id": worker_message.message_id,
        }
        await callback.answer(text=messages["status_updated_successfully"], show_alert=True)

        user_message = await send_application(
            bot,
            int(application.user_telegram_id),
            text=messages["assigned_application_notification_for_user"](
                application, motorcycle, promo_code
            ),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )
        data["user"] = {
            "chat_id": user_message.chat.id,
            "message_id": user_message.message_id,
        }
        data["admins"] = []

        for admin in admins:
            admin_message = await send_application(
                bot,
                int(admin.telegram_id),
                text=messages["in_progress_application_notification_for_admin"](
                    application, user, motorcycle, promo_code
                ),
                reply_markup=keyboards["admin_cancel_app"](application_number),
                photo_id=application.photo_id,
                video_id=application.video_id,
            )
            data["admins"].append(
                {
                    "chat_id": admin_message.chat.id,
                    "message_id": admin_message.message_id,
                }
            )

        await redis.set(str(application.id), json.dumps(data))

    except Exception as e:
        log.error(f"Error updating application status: {e}")
        await callback.answer(text=messages["status_update_error"], show_alert=True)


class PhotoResult(StatesGroup):
    photo_result = State()


@router.callback_query(
    lambda callback_name: callback_name.data.startswith("completed_application:")
)
async def change_status_completed_application_callback(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    state: FSMContext,
):
    application_number = int(callback.data.split(":")[1])
    try:
        application = await application_service.get_by_number(application_number)
        if not application:
            raise ValueError(f"Application with number {application_number} not found")
        await application_service.update({"status": Status.COMPLETED}, application.id)
        await state.set_state(PhotoResult.photo_result)
        await state.update_data(application_id=str(application.id))
        await callback.answer(text=messages["status_updated_successfully"], show_alert=True)
        await callback.message.answer(text=messages["add_photo_result"])
        await callback.message.delete()
    except Exception as e:
        log.error(f"Error updating application status: {e}")
        await callback.answer(text=messages["status_update_error"], show_alert=True)


@router.message(StateFilter(PhotoResult.photo_result))
async def getting_photo_result(
    message: Message,
    state: FSMContext,
    messages: dict,
    application_service: ApplicationService,
    user_service: UserService,
    motorcycle_service: MotorcycleService,
    promo_code_service: PromoCodeService,
    redis: Redis,
    bot: Bot,
    keyboards: dict,
):
    photo_result_id = None
    data = await state.get_data()
    application_id = data["application_id"]
    if message.content_type == "photo":
        photo_result_id = message.photo[-1].file_id
    if not photo_result_id:
        await message.answer(
            text=messages["photo_result_not_valid"],
        )
        return
    try:
        application = await application_service.update(
            {"photo_result_id": photo_result_id},
            item_id=application_id
        )
        user = await user_service.get_by_telegram_id(str(application.user_telegram_id))
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        promo_code = (
            await promo_code_service.get(application.promo_code_id)
            if application.promo_code_id
            else None
        )
        admins = await user_service.get_admins()

        data = await redis.get(str(application.id))
        data = json.loads(data) if data else {"admins": [], "user": {}, "worker": {}}
        try:
            await bot.delete_message(
                int(data["user"]["chat_id"]),
                int(data["user"]["message_id"]),
            )
            for admin in data["admins"]:
                await bot.delete_message(
                    int(admin["chat_id"]),
                    int(admin["message_id"]),
                )
        except Exception as e:
            log.error(f"Error deleting previous messages: {e}")

        await send_application(
            bot,
            message.chat.id,
            text=messages["assigned_application_notification_for_worker"](
                application, user, motorcycle, promo_code
            ),
            photo_id=photo_result_id
        )

        data = {"admins": []}

        for admin in admins:
            admin_message = await send_application(
                bot,
                int(admin.telegram_id),
                text=messages["completed_application_notification_for_admin"](
                    application, user, motorcycle, promo_code
                ),
                photo_id=application.photo_result_id,
                reply_markup=keyboards['confirm_completion'](application.number),
            )
            data["admins"].append(
                {
                    "chat_id": admin_message.chat.id,
                    "message_id": admin_message.message_id,
                }
            )
        await redis.set(str(application.id), json.dumps(data))
    except Exception as e:
        log.error(f"Error updating photo result: {e}")

    await state.clear()

@router.callback_query(
    lambda callback_name: callback_name.data.startswith("confirm_completion:")
)
async def confirm_completion(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    bot: Bot,
    motorcycle_service: MotorcycleService,
    promo_code_service: PromoCodeService,
    user_service: UserService,
    redis: Redis
):
    application_number = int(callback.data.split(":")[1])
    try:
        application = await application_service.get_by_number(application_number)
        if not application:
            raise ValueError(f"Application with number {application_number} not found")
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        promo_code = await promo_code_service.get(application.promo_code_id) if application.promo_code_id else None
        user = await user_service.get_by_telegram_id(application.user_telegram_id)
        await send_application(
            bot,
            int(application.user_telegram_id),
            text=messages["completed_application_notification_for_user"](
                application, motorcycle, promo_code
            ),
            photo_id=application.photo_result_id,
        )
        data = await redis.get(str(application.id))
        data = json.loads(data) if data else {"admins": []}
        try:
            for admin in data["admins"]:
                await bot.delete_message(
                    int(admin["chat_id"]),
                    int(admin["message_id"]),
                )
        except Exception as e:
            log.error(f"Error deleting previous messages: {e}")

        for admin in data["admins"]:
            await send_application(
                bot,
                int(admin["chat_id"]),
                text=messages["completed_application_notification_for_admin"](
                    application, user, motorcycle, promo_code
                ),
                photo_id=application.photo_result_id,
            )

    except Exception as e:
        log.error(f"Error getting application: {e}")


@router.callback_query(
    lambda callback_name: callback_name.data.startswith("evacuation_in_progress:")
)
async def change_status_in_progress_evacuation_callback(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    keyboards: dict,
    bot: Bot,
    motorcycle_service: MotorcycleService,
    user_service: UserService,
    redis: Redis,
):
    application_number = int(callback.data.split(":")[1])
    try:
        application = await application_service.get_by_number(application_number)
        if not application:
            raise ValueError(f"Application with number {application_number} not found")
        user = await user_service.get_by_telegram_id(str(application.user_telegram_id))
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        await application_service.update({"status": Status.IN_PROGRESS}, application.id)
        data = await redis.get(str(application.id))
        data = json.loads(data) if data else {"admins": [], "user": {}, "worker": {}}
        try:
            await bot.delete_message(
                int(data["user"]["chat_id"]),
                int(data["user"]["message_id"]),
            )
            for admin in data["admins"]:
                await bot.delete_message(
                    int(admin["chat_id"]),
                    int(admin["message_id"]),
                )
        except Exception as e:
            log.error(f"Error deleting previous messages: {e}")

        data["admins"] = []
        admin_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=messages["evacuation_application_notification_for_admin"](
                application, user, motorcycle
            ),
            reply_markup=keyboards["evacuation_completed"](application.number),
        )
        data["admins"].append(
            {
                "chat_id": admin_message.chat.id,
                "message_id": admin_message.message_id,
            }
        )
        await callback.answer(text=messages["status_updated_successfully"], show_alert=True)

        user_message = await bot.send_message(
            chat_id=application.user_telegram_id,
            text=messages["evacuation_in_progress"](
                motorcycle.motorcycle_model,
                application.description,
                application.status,
                application.location,
            ),
            reply_markup=keyboards["application_evacuation"](application.id),
        )
        data["user"] = {
            "chat_id": user_message.chat.id,
            "message_id": user_message.message_id,
        }

        await redis.set(str(application.id), json.dumps(data))

    except Exception as e:
        log.error(f"Error updating application status: {e}")
        await callback.answer(text=messages["status_update_error"], show_alert=True)


@router.callback_query(lambda callback_name: callback_name.data.startswith("completed_evacuation:"))
async def change_status_completed_evacuation_callback(
    callback: CallbackQuery,
    application_service: ApplicationService,
    messages: dict,
    bot: Bot,
    motorcycle_service: MotorcycleService,
    user_service: UserService,
    redis: Redis,
):
    application_number = int(callback.data.split(":")[1])
    try:
        application = await application_service.get_by_number(application_number)
        if not application:
            raise ValueError(f"Application with number {application_number} not found")
        user = await user_service.get_by_telegram_id(str(application.user_telegram_id))
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        await application_service.update({"status": Status.COMPLETED}, application.id)
        data = await redis.get(str(application.id))
        data = json.loads(data) if data else {"admins": [], "user": {}, "worker": {}}
        try:
            await bot.delete_message(
                int(data["user"]["chat_id"]),
                int(data["user"]["message_id"]),
            )
            for admin in data["admins"]:
                await bot.delete_message(
                    int(admin["chat_id"]),
                    int(admin["message_id"]),
                )
        except Exception as e:
            log.error(f"Error deleting previous messages: {e}")

        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=messages["evacuation_application_notification_for_admin"](
                application, user, motorcycle
            ),
        )
        await callback.answer(text=messages["status_updated_successfully"], show_alert=True)

        await bot.send_message(
            chat_id=int(application.user_telegram_id),
            text=messages["evacuation_completed"](
                motorcycle.motorcycle_model,
                application.description,
                application.status,
                application.location,
            ),
        )
        await redis.delete(str(application.id))

    except Exception as e:
        log.error(f"Error updating application status: {e}")
        await callback.answer(text=messages["status_update_error"], show_alert=True)
