from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import PromoCodeModel
from .repositories import PromoCodeRepository


class PromoCodeService(SQLAlchemyAsyncRepositoryService[PromoCodeModel, PromoCodeRepository]):
    """PromoCode Service"""

    repository_type = PromoCodeRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)
