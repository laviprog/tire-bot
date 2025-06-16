from datetime import datetime, timezone

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import PromoCodeModel
from .repositories import PromoCodeRepository


class PromoCodeService(SQLAlchemyAsyncRepositoryService[PromoCodeModel, PromoCodeRepository]):
    """PromoCode Service"""

    repository_type = PromoCodeRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)

    async def mark_as_used(self, promo_code: str) -> None:
        """
        Mark the promo code as used.
        :param promo_code: The promo code to mark as used.
        """
        promo = await self.get_one_or_none(PromoCodeModel.code == promo_code)

        if not promo:
            return

        promo.used_count += 1
        await self.update(promo)

    async def validate(self, promo_code: str) -> bool:
        """
        Validate the promo code.
        :param promo_code: The promo code to validate.
        :return: True if the promo code is valid, False otherwise.
        """
        promo = await self.get_one_or_none(PromoCodeModel.code == promo_code)

        if not promo:
            return False

        now = datetime.now(timezone.utc)

        if not promo.is_active:
            return False

        if promo.valid_from and promo.valid_from > now:
            return False
        if promo.valid_until and promo.valid_until < now:
            return False

        if promo.usage_limit is not None and promo.used_count >= promo.usage_limit:
            return False

        return True
