from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import UserModel
from .repositories import UserRepository


class UserService(SQLAlchemyAsyncRepositoryService[UserModel, UserRepository]):
    """User Service"""

    repository_type = UserRepository
