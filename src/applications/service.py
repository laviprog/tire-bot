from datetime import datetime, timedelta, timezone
from uuid import UUID

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from .models import ApplicationModel, Status
from .repositories import ApplicationRepository


class ApplicationService(SQLAlchemyAsyncRepositoryService[ApplicationModel, ApplicationRepository]):
    """Application Service"""

    repository_type = ApplicationRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)

    async def cancel(self, application_id: UUID) -> ApplicationModel:
        """Cancel application by ID"""
        return await self.update(
            {
                "status": Status.CANCELLED,
            },
            application_id,
        )

    async def get_by_number(self, number: int) -> ApplicationModel | None:
        """Get application by number"""
        return await self.get_one_or_none(ApplicationModel.number == number)

    async def get_list_created_within(self, duration: timedelta) -> list[ApplicationModel]:
        """List applications created within the last `duration`."""
        return (
            await self.list(
                ApplicationModel.created_at > datetime.now(tz=timezone.utc) - duration,
                order_by=ApplicationModel.number.asc(),
            )
            or []
        )
