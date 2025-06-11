from aiogram import Dispatcher

from .command import router as command_router
from .profile import router as profile_router
from .back import router as back_router


def register_handlers(dp: Dispatcher):
    dp.include_router(command_router)
    dp.include_router(profile_router)
    dp.include_router(back_router)
