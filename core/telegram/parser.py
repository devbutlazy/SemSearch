from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

from core.config import settings
from core.database.models.message import MessageORM
from core.database.repositories.message import MessageRepository
from core.telegram import logger


class MessageParser:
    def __init__(self) -> None:
        self.client = TelegramClient(
            settings.SESSION_NAME, settings.API_ID, settings.API_HASH
        )

    async def _store_message(self, message: Message) -> None:
        if getattr(message, "from_id", None) is None or not hasattr(message.from_id, "user_id"):
            return None

        logger.info(f"Fetched: {message.text} | {message.id}")

        async with MessageRepository() as repository:
            await repository.add_message(
                MessageORM(
                    message_id=message.id,
                    message_text=message.message,
                    message_date=message.date,
                    from_chat_id=message.chat_id,
                    from_user_id=message.from_id.user_id,
                    embedding=None,
                )
            )

    def _setup_event_handler(self) -> None:
        @self.client.on(events.NewMessage(chats=settings.CHAT_ID))
        async def _(event: events.NewMessage.Event) -> None:
            await self._store_message(event.message)

    async def sync_messages(
        self,
        reverse: bool = True,
    ) -> None:
        await self.client.start()

        try:
            await self.client.get_entity(settings.CHAT_ID)
        except ValueError:
            await self.client.get_dialogs()

        async for message in self.client.iter_messages(
            entity=settings.CHAT_ID,
            reverse=reverse,
        ):
            await self._store_message(message)

        logger.info("Listening for new messages…")

        self._setup_event_handler()
        await self.client.run_until_disconnected()
