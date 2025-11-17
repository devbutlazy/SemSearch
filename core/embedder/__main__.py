import asyncio
import logging

from core.embedder.services.model import EmbeddingModel
from core.embedder.services.repository import MessageService
from core.embedder.services.orchestrator import EmbeddingOrchestrator
from core.embedder.services.search import SearchService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    model = EmbeddingModel(max_length=1024)
    repository_service = MessageService()
    orchestrator = EmbeddingOrchestrator(model, repository_service, batch_size=1024)

    await orchestrator.run(interval_sec=30)


async def search_via_query(): # ! TEST
    model = EmbeddingModel(max_length=1024)
    repository_service = MessageService()
    search_service = SearchService(model, repository_service)

    query = input(">>> ")
    results = sorted(
        await search_service.search(query, limit=50),
        key=lambda result: int(result["id"]),
    )

    if not results:
        print("Nothing found :(")
        return None

    for index, result in enumerate(results):
        print(f"{index}) {result["date"].strftime("%d %b %H:%M")} - {result["link"]}")


if __name__ == "__main__":
    asyncio.run(search_via_query()) # ! OR search_via_query
