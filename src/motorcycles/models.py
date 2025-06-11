from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from uuid import UUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from src.users.models import UserModel


class MotorcycleModel(UUIDAuditBase):
    """Motorcycle model."""

    __tablename__ = "motorcycles"

    name: Mapped[str] = mapped_column(String(128))
    year: Mapped[int]
    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    engine: Mapped[str] = mapped_column(String(50))
    user_telegram_id: Mapped[UUID] = mapped_column(ForeignKey("users.telegram_id"), nullable=False)

    owner: Mapped["UserModel"] = relationship(back_populates="motorcycles")
