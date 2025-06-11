from aiogram import Dispatcher

from .motorcycle_service import MotorcycleServiceMiddleware
from .redis import RedisMiddleware
from .user_service import UserServiceMiddleware
from src.database import sqlalchemy_config


def register_middlewares(dp: Dispatcher, **kwargs):
    dp.update.middleware(RedisMiddleware(kwargs["redis"]))
    dp.update.middleware(UserServiceMiddleware(config=sqlalchemy_config))
    dp.update.middleware(MotorcycleServiceMiddleware(config=sqlalchemy_config))
