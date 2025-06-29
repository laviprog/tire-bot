from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import ApplicationModel, Status
from .repositories import ApplicationRepository


class ApplicationService(SQLAlchemyAsyncRepositoryService[ApplicationModel, ApplicationRepository]):
    """Application Service"""

    repository_type = ApplicationRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)

    async def cancel(self, application_id: str) -> None:
        await self.update(
            {
                "status": Status.CANCELLED,
            },
            application_id
        )
