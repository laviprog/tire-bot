import json
from uuid import UUID

from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from redis.asyncio import Redis

from src import log
from src.applications import ApplicationService, Status
from src.bot.handlers.keyboards import SKIP
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


class CommentState(StatesGroup):
    comment = State()


@router.callback_query(lambda callback_name: callback_name.data.startswith("select_worker:"))
async def admin_assigned_worker(
    callback: CallbackQuery,
    user_service: UserService,
    application_service: ApplicationService,
    state: FSMContext,
    messages: dict,
    keyboards: dict,
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
        application = await application_service.update(
            {
                "status": Status.ASSIGNED,
                "worker_telegram_id": worker.telegram_id,
            },
            item_id=application.id,
        )
        await state.update_data(application_id=str(application.id))
        await state.set_state(CommentState.comment)
        await callback.message.answer(
            text=messages["add_admin_comment"],
            reply_markup=keyboards["skip_step"],
        )

    except Exception as e:
        await callback.answer(text=messages["assign_application_error"], show_alert=True)
        log.error(
            f"Ошибка при назначении работника на заказ. Application: {application_number}, Worker username: {worker_username}. Error: {e}"
        )
        return


@router.message(StateFilter(CommentState.comment))
async def add_admin_comment(
    message: Message,
    state: FSMContext,
    application_service: ApplicationService,
    user_service: UserService,
    motorcycle_service: MotorcycleService,
    promo_code_service: PromoCodeService,
    messages: dict,
    redis: Redis,
    bot: Bot,
    keyboards: dict,
):
    comment = message.text.strip()
    data = await state.get_data()
    application_id = UUID(data["application_id"])
    if comment not in SKIP:
        try:
            await application_service.update({"admin_comment": comment}, item_id=application_id)
            await message.answer(
                text=messages["admin_comment_has_been_added"],
                reply_markup=keyboards["admin_main_menu"],
            )
        except Exception as e:
            await message.answer(
                text=messages["add_admin_comment_error"],
                reply_markup=keyboards["admin_main_menu"],
            )
            log.error(f"Error adding comment to application {application_id}: {e}")

    await state.clear()

    data = await redis.get(str(application_id))
    data = json.loads(data) if data else {"admins": [], "user": {}, "worker": {}}
    try:
        await bot.delete_message(int(data["user"]["chat_id"]), int(data["user"]["message_id"]))
        for admin in data["admins"]:
            await bot.delete_message(int(admin["chat_id"]), int(admin["message_id"]))
    except Exception as e:
        log.error(f"Error deleting previous messages: {e}")

    try:
        application = await application_service.get(application_id)
        admins = await user_service.get_admins()
        user = await user_service.get_by_telegram_id(application.user_telegram_id)
        if not user:
            raise ValueError(f"User with telegram ID {application.user_telegram_id} not found")
        motorcycle = await motorcycle_service.get(application.motorcycle_id)
        promo_code = (
            await promo_code_service.get(application.promo_code_id)
            if application.promo_code_id
            else None
        )
        worker = await user_service.get_by_telegram_id(application.worker_telegram_id)
        if not worker:
            raise ValueError(f"Worker with telegram ID {application.worker_telegram_id} not found")
        application_number = application.number

        data["admins"] = []
        for admin in admins:
            admin_message = await send_application(
                bot,
                admin.chat_id,
                text=messages["assigned_application_notification_for_admin"](
                    application, user, motorcycle, promo_code, worker
                ),
                reply_markup=keyboards["admin_cancel_app"](application_number),
                photo_id=application.photo_id,
                video_id=application.video_id,
            )
            data["admins"].append(
                {"chat_id": admin_message.chat.id, "message_id": admin_message.message_id}
            )
        worker_message = await send_application(
            bot,
            int(worker.chat_id),
            text=messages["assigned_application_notification_for_worker"](
                application, user, motorcycle, promo_code
            ),
            reply_markup=keyboards["worker_in_progress"](application_number),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )
        data["worker"] = {
            "chat_id": worker_message.chat.id,
            "message_id": worker_message.message_id,
        }
        user_message = await send_application(
            bot,
            int(user.telegram_id),
            text=messages["assigned_application_notification_for_user"](
                application, motorcycle, promo_code
            ),
            # reply_markup=keyboards["application"](application.id),
            photo_id=application.photo_id,
            video_id=application.video_id,
        )
        data["user"] = {"chat_id": user_message.chat.id, "message_id": user_message.message_id}

        await redis.set(str(application.id), json.dumps(data))
    except Exception as e:
        log.error(f"Error sending assigned application messages: {e}")
        return
