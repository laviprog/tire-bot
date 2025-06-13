from aiogram import Dispatcher

from .delete_motorcycle import router as delete_motorcycle_router
from .register import router as motorcycles_registration_router
from .edit_motorcycle import router as edit_motorcycle_router


def register_handlers(dp: Dispatcher):
    dp.include_router(delete_motorcycle_router)
    dp.include_router(motorcycles_registration_router)
    dp.include_router(edit_motorcycle_router)
