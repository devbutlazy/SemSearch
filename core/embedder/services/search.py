from typing import Any

from core.database.models.message import MessageORM
from core.embedder.services.model import EmbeddingModel
from core.embedder.services.repository import MessageService


class SearchService:
    def __init__(self, model: EmbeddingModel, repo_service: MessageService) -> None:
        self.model = model
        self.repo_service = repo_service

    async def search(self, query: str, limit: int = 50) -> list[dict[str, Any]]:
        query_vec = self.model.embed_text(query).tolist()
        messages: list[MessageORM] = await self.repo_service.search_by_embedding(
            query_vec, limit
        )

        results: list[dict[str, Any]] = []
        for message in messages:
            link = f"https://t.me/c/{message.from_chat_id}/{message.message_id}"
            results.append(
                {
                    "id": message.message_id,
                    "from_user": message.from_user_id,
                    "text": message.message_text,
                    "date": message.message_date,
                    "link": link,
                }
            )

        return results
