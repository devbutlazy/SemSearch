import asyncio

from core.embedder import logger

from core.embedder.services.model import EmbeddingModel
from core.embedder.services.repository import MessageService
from core.database.models.message import MessageORM


class EmbeddingOrchestrator:
    def __init__(
        self, model: EmbeddingModel, repo_service: MessageService, batch_size: int = 256
    ):
        self.model = model
        self.repo_service = repo_service
        self.batch_size = batch_size

    async def run_cycle(self) -> None:
        messages: list[MessageORM] = await self.repo_service.get_unembedded_messages()
        if not messages:
            logger.info("No messages to embed.")
            return None

        logger.info(f"Fetched {len(messages)} messages without embeddings.")

        texts = [msg.message_text or "" for msg in messages]

        for i in range(0, len(texts), self.batch_size):
            batch_msgs = messages[i : i + self.batch_size]
            batch_texts = texts[i : i + self.batch_size]

            logger.info(f"Processing batch {i}-{i + len(batch_texts)}")
            batch_vecs = self.model.embed_texts(batch_texts, batch_size=self.batch_size)

            for msg, vec in zip(batch_msgs, batch_vecs):
                msg.embedding = vec.tolist()

            await self.repo_service.save_embeddings_bulk(batch_msgs)
            logger.info(f"Updated embeddings for batch {i}-{i + len(batch_texts)}")

    async def run(self, interval_sec: int = 30) -> None:
        while True:
            try:
                await self.run_cycle()
            except BaseException as error:
                logger.exception(f"Error during embedding cycle: {error}")
            await asyncio.sleep(interval_sec)
