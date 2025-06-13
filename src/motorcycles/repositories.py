from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from .models import MotorcycleModel


class MotorcycleRepository(SQLAlchemyAsyncRepository[MotorcycleModel]):
    """Motorcycle repository"""

    model_type = MotorcycleModel
