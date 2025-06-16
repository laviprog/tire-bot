from aiogram import Dispatcher

from .promo_codes import register_handlers as register_promo_codes_handlers


def register_handlers(dp: Dispatcher):
    register_promo_codes_handlers(dp)
