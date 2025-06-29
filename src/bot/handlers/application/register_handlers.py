from aiogram import Dispatcher

from .create import router as create_router
from .cancel import router as cancel_router


def register_handlers(dp: Dispatcher):
    dp.include_router(create_router)
    dp.include_router(cancel_router)
