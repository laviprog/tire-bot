from aiogram import Dispatcher

from .command import router as command_router
from .back import router as back_router
from .motorcycles import register_handlers as register_motorcycles_handlers
from .users import register_handlers as register_users_handlers


def register_handlers(dp: Dispatcher):
    dp.include_router(command_router)
    dp.include_router(back_router)
    register_motorcycles_handlers(dp)
    register_users_handlers(dp)
