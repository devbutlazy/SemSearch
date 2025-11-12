import asyncio
import logging

from core.database import init_db
from core.telegram.services.parser import MessageParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Initializing Telegram parser...")
    await init_db()
    await MessageParser().sync_messages()


if __name__ == "__main__":
    asyncio.run(main())
