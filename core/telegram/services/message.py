from typing import Optional

from telethon.tl.custom.message import Message

from core.telegram import logger
from core.database.repositories.message import MessageRepository
from core.database.models.message import MessageORM


class MessageService:
    def __init__(self, repository: Optional[MessageRepository] = None):
        self.repository = repository

    async def store_message(self, message: Message) -> None:
        if not getattr(message, "from_id", None) or not hasattr(
            message.from_id, "user_id"
        ):
            return None

        logger.info(f"Fetched new message: {message.text} | {message.id}")

        async with MessageRepository() as repository:
            await repository.add_message(
                MessageORM(
                    message_id=message.id,
                    message_text=message.message,
                    message_date=message.date,
                    from_chat_id=message.peer_id.channel_id,
                    from_user_id=message.from_id.user_id,
                    embedding=None,
                )
            )

    async def get_last_message_id(self) -> Optional[int]:
        async with MessageRepository() as repo:
            return await repo.get_last_message_id()
