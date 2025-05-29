from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from .models import UserModel


class UserRepository(SQLAlchemyAsyncRepository[UserModel]):
    """User repository"""

    model_type = UserModel
