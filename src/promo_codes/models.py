from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum

if TYPE_CHECKING:
    from src.applications.models import ApplicationModel


class DiscountType(str, Enum):
    """Enum for discount types."""

    PERCENTAGE = "percentage"
    FIXED = "fixed"


class PromoCodeModel(UUIDAuditBase):
    """PromoCode model."""

    __tablename__ = "promo_codes"

    code: Mapped[str] = mapped_column(unique=True, index=True)
    discount_type: Mapped[DiscountType | None] = mapped_column(
        SQLAlchemyEnum(DiscountType), default=DiscountType.PERCENTAGE
    )
    discount_value: Mapped[float | None] = mapped_column(default=None)
    usage_limit: Mapped[int | None] = mapped_column(default=None)
    used_count: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    valid_from: Mapped[datetime | None] = mapped_column(default=None)
    valid_until: Mapped[datetime | None] = mapped_column(default=None)

    applications: Mapped[list["ApplicationModel"]] = relationship(
        back_populates="promo_code", lazy="selectin"
    )
