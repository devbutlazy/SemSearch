import asyncio
import logging

from core.database import init_db
from core.telegram.parser import BaseClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting the main process...")
    await init_db()
    await BaseClient().parse()

if __name__ == "__main__":
    asyncio.run(main())
