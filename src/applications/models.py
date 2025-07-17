from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey, String, Integer, Sequence

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
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


STATUS_MAP = {
    Status.NEW: "Новая заявка",
    Status.ASSIGNED: "Назначен специалист",
    Status.IN_PROGRESS: "В работе",
    Status.COMPLETED: "Завершено",
    Status.CANCELLED: "Отменено",
}


class ApplicationModel(UUIDAuditBase):
    """Application model."""

    __tablename__ = "applications"

    number: Mapped[int] = mapped_column(
        Integer, Sequence("application_number_seq"), unique=True, index=True
    )
    type: Mapped[Type] = mapped_column(SQLAlchemyEnum(Type), default=Type.SERVICE)
    status: Mapped[Status] = mapped_column(SQLAlchemyEnum(Status), default=Status.NEW)
    description: Mapped[str | None]
    photo_id: Mapped[str | None]
    video_id: Mapped[str | None]
    service_datetime: Mapped[datetime | None]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    location: Mapped[str | None]

    user_telegram_id: Mapped[str] = mapped_column(ForeignKey("users.telegram_id"), nullable=False)
    worker_telegram_id: Mapped[str] = mapped_column(String(64), nullable=True)
    motorcycle_id: Mapped[UUID | None] = mapped_column(ForeignKey("motorcycles.id"))
    promo_code_id: Mapped[UUID | None] = mapped_column(ForeignKey("promo_codes.id"))

    owner: Mapped["UserModel"] = relationship(back_populates="applications")
    motorcycle: Mapped["MotorcycleModel | None"] = relationship(back_populates="applications")
    promo_code: Mapped["PromoCodeModel | None"] = relationship(back_populates="applications")
