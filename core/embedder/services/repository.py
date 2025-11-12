from core.database.repositories.message import MessageRepository
from core.database.models.message import MessageORM


class MessageService:
    """Database service to fetch/update messages with embeddings."""

    def __init__(self):
        self.repository_cls = MessageRepository

    async def get_unembedded_messages(self) -> list[MessageORM]:
        async with self.repository_cls() as repo:
            return await repo.get_unembedded_messages()

    async def save_embeddings_bulk(self, messages: list[MessageORM]):
        async with self.repository_cls() as repo:
            await repo.add_messages_bulk(messages)
