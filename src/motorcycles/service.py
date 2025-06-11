from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import MotorcycleModel
from .repositories import MotorcycleRepository


class MotorcycleService(SQLAlchemyAsyncRepositoryService[MotorcycleModel, MotorcycleRepository]):
    """Motorcycle Service"""

    repository_type = MotorcycleRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)
