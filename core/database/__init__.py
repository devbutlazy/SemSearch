import logging

from sqlalchemy.ext.asyncio import create_async_engine

from core.config import settings
from core.database.models.base import Base

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.DB_URL,
)


async def init_db() -> None:
    """
    Initialize database via Base-model metadata
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schema initialized successfully.")
    except BaseException as error:
        logger.exception(f"Error initializing database schema: {error}")
