from aiogram import Dispatcher

from .command import router as command_router


def register_handlers(dp: Dispatcher):
    dp.include_router(command_router)
