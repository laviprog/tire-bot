from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import UserModel, Role
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

    async def get_role_by_telegram_id(self, telegram_id: str) -> Role | None:
        """Get user role by telegram ID"""
        user = await self.get_by_telegram_id(telegram_id=telegram_id)
        if user is None:
            return None
        return user.role

    async def is_admin_by_telegram_id(self, telegram_id: str) -> bool:
        """Check if user is admin by telegram ID"""
        role = await self.get_role_by_telegram_id(telegram_id=telegram_id)
        return role is not None and role == Role.ADMIN

    async def is_user_by_telegram_id(self, telegram_id: str) -> bool:
        """Check if user is user by telegram ID"""
        role = await self.get_role_by_telegram_id(telegram_id=telegram_id)
        return role is not None and role == Role.USER

    async def is_worker_by_telegram_id(self, telegram_id: str) -> bool:
        """Check if user is worker by telegram ID"""
        role = await self.get_role_by_telegram_id(telegram_id=telegram_id)
        return role is not None and role == Role.WORKER
