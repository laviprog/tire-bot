from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from src.users.models import UserModel
    from src.applications.models import ApplicationModel


class MotorcycleModel(UUIDAuditBase):
    """Motorcycle model."""

    __tablename__ = "motorcycles"

    year: Mapped[int]
    motorcycle_model: Mapped[str] = mapped_column(String(128))
    user_telegram_id: Mapped[str] = mapped_column(ForeignKey("users.telegram_id"), nullable=False)

    owner: Mapped["UserModel"] = relationship(back_populates="motorcycles")
    applications: Mapped[list["ApplicationModel"]] = relationship(
        back_populates="motorcycle", cascade="all, delete-orphan", lazy="selectin"
    )
