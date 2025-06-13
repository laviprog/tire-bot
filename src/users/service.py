from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import UserModel
from .repositories import UserRepository


class UserService(SQLAlchemyAsyncRepositoryService[UserModel, UserRepository]):
    """User Service"""

    repository_type = UserRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)

    async def get_by_telegram_id(self, telegram_id: str) -> UserModel | None:
        """Get user by telegram ID"""
        return await self.repository.get_one_or_none(UserModel.telegram_id == telegram_id)
