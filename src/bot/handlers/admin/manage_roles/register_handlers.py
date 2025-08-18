from aiogram import Dispatcher

from .add import router as add_router
from .menu import router as menu_router
from .view import router as view_router


def register_handlers(dp: Dispatcher):
    dp.include_router(add_router)
    dp.include_router(menu_router)
    dp.include_router(view_router)
