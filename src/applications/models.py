from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey

if TYPE_CHECKING:
    from src.users.models import UserModel
    from src.motorcycles.models import MotorcycleModel  # noqa
    from src.promo_codes.models import PromoCodeModel  # noqa


class Type(str, Enum):
    """Enum for application types."""

    SERVICE = "service"
    EVACUATION = "evacuation"


class Status(str, Enum):
    """Enum for application statuses."""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ApplicationModel(UUIDAuditBase):
    """Application model."""

    __tablename__ = "applications"

    type: Mapped[Type] = mapped_column(SQLAlchemyEnum(Type), default=Type.SERVICE)
    status: Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.NEW)
    description: Mapped[str | None]
    photo_id: Mapped[str | None]
    video_id: Mapped[str | None]
    service_datetime: Mapped[datetime | None]

    user_telegram_id: Mapped[str] = mapped_column(ForeignKey("users.telegram_id"), nullable=False)
    motorcycle_id: Mapped[UUID | None] = mapped_column(ForeignKey("motorcycles.id"))
    promo_code_id: Mapped[UUID | None] = mapped_column(ForeignKey("promo_codes.id"))

    owner: Mapped["UserModel"] = relationship(back_populates="applications")
    motorcycle: Mapped["MotorcycleModel | None"] = relationship(back_populates="applications")
    promo_code: Mapped["PromoCodeModel | None"] = relationship(back_populates="applications")
