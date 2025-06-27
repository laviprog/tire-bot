from aiogram import Dispatcher

from .application_service import ApplicationServiceMiddleware
from .bot import BotMiddleware
from .languages import LanguageMiddleware
from .motorcycle_service import MotorcycleServiceMiddleware
from .promo_code_service import PromoCodeServiceMiddleware
from .redis import RedisMiddleware
from .user_service import UserServiceMiddleware
from src.database import sqlalchemy_config


def register_middlewares(dp: Dispatcher, **kwargs):
    dp.update.middleware(RedisMiddleware(kwargs["redis"]))
    dp.update.middleware(UserServiceMiddleware(config=sqlalchemy_config))
    dp.update.middleware(MotorcycleServiceMiddleware(config=sqlalchemy_config))
    dp.update.middleware(PromoCodeServiceMiddleware(config=sqlalchemy_config))
    dp.update.middleware(ApplicationServiceMiddleware(config=sqlalchemy_config))
    dp.update.middleware(LanguageMiddleware())
    dp.update.middleware(BotMiddleware())
