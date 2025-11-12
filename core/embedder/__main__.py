import asyncio
import logging

from core.embedder.services.model import EmbeddingModel
from core.embedder.services.repository import MessageService
from core.embedder.services.orchestrator import EmbeddingOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    model = EmbeddingModel(max_length=4096)
    repository_service = MessageService()
    orchestrator = EmbeddingOrchestrator(model, repository_service, batch_size=256)

    await orchestrator.run(interval_sec=30)


if __name__ == "__main__":
    asyncio.run(main())
