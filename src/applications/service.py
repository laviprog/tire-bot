from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import ApplicationModel
from .repositories import ApplicationRepository


class ApplicationService(SQLAlchemyAsyncRepositoryService[ApplicationModel, ApplicationRepository]):
    """Application Service"""

    repository_type = ApplicationRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)
