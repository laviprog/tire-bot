from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from .models import ApplicationModel


class ApplicationRepository(SQLAlchemyAsyncRepository[ApplicationModel]):
    """Application repository"""

    model_type = ApplicationModel
