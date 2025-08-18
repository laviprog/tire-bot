from aiogram import Dispatcher

from .promo_codes import register_handlers as register_promo_codes_handlers
from .admin_settings import router as admin_settings_router
from .manage_roles import register_handlers as register_manage_roles_handlers
from .view import router as view_router


def register_handlers(dp: Dispatcher):
    register_promo_codes_handlers(dp)
    register_manage_roles_handlers(dp)
    dp.include_router(admin_settings_router)
    dp.include_router(view_router)
