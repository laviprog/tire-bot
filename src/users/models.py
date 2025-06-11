from enum import Enum
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Boolean
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from src.motorcycles.models import MotorcycleModel


class Role(str, Enum):
    """User roles."""

    ADMIN = "admin"
    USER = "user"


class UserModel(UUIDAuditBase):
    """User model."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    telegram_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(128))
    phone_number: Mapped[str | None] = mapped_column(String(32))
    role: Mapped[Role] = mapped_column(SQLAlchemyEnum(Role), default=Role.USER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    motorcycles: Mapped[list["MotorcycleModel"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan", lazy="selectin"
    )
