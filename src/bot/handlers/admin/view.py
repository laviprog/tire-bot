from datetime import timedelta

from aiogram import Router
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

from src.applications import ApplicationService
from src.bot.filters import Text
from src.bot.handlers.keyboards import LIST_APPLICATIONS_LAST_2_WEEKS
from src.users import UserService

router = Router()


@router.message(Text(LIST_APPLICATIONS_LAST_2_WEEKS))
async def list_application_last_2_weeks(
    message: Message,
    messages: dict,
    application_service: ApplicationService,
    user_service: UserService,
):
    applications_for_last_2_weeks = await application_service.get_list_created_within(
        timedelta(weeks=2)
    )
    if not applications_for_last_2_weeks:
        await message.answer(messages["no_applications_last_2_weeks"])
        return

    for application in applications_for_last_2_weeks:
        worker = await user_service.get_by_telegram_id(application.worker_telegram_id)
        user = application.owner
        motorcycle = application.motorcycle
        promo_code = application.promo_code
        if application.photo_id or application.photo_result_id:
            media_group = MediaGroupBuilder(
                caption=messages["application_info"](
                    application, worker, user, motorcycle, promo_code
                )
            )
            if application.photo_id:
                media_group.add_photo(media=application.photo_id)
            if application.photo_result_id:
                media_group.add_photo(media=application.photo_result_id)
            await message.answer_media_group(media=media_group.build())
        else:
            await message.answer(
                messages["application_info"](application, worker, user, motorcycle, promo_code),
            )
