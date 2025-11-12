import asyncio
import logging

from core.embedding.embedder import Embedder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

async def main() -> None:
    logger.info("Initializing embedding system")
    embedder = Embedder(4096, 256)

    while True:
        await embedder.run()
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
