from advanced_alchemy.config import AsyncSessionConfig, SQLAlchemyAsyncConfig

from src.config import settings

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.PG_URL,
    session_config=session_config,
)
