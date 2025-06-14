from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from .models import PromoCodeModel


class PromoCodeRepository(SQLAlchemyAsyncRepository[PromoCodeModel]):
    """PromoCode repository"""

    model_type = PromoCodeModel
