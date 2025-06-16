from aiogram import Dispatcher

from .delete import router as delete_router
from .create import router as create_router
from .edit import router as edit_router
from .menu import router as menu_router


def register_handlers(dp: Dispatcher):
    dp.include_router(delete_router)
    dp.include_router(create_router)
    dp.include_router(edit_router)
    dp.include_router(menu_router)
