from aiogram import Dispatcher

from .register import router as user_registration_router
from .edit import router as edit_user_router


def register_handlers(dp: Dispatcher):
    dp.include_router(user_registration_router)
    dp.include_router(edit_user_router)
