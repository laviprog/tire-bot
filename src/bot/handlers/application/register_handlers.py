from aiogram import Dispatcher

from .create import router as create_router
from .cancel import router as cancel_router
from .add_worker import router as add_worker_router
from .update import router as update_router


def register_handlers(dp: Dispatcher):
    dp.include_router(create_router)
    dp.include_router(cancel_router)
    dp.include_router(add_worker_router)
    dp.include_router(update_router)
