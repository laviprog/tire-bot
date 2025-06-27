from aiogram import Dispatcher

from .create import router as create_router


def register_handlers(dp: Dispatcher):
    dp.include_router(create_router)
