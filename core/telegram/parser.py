from typing import Any, Dict, Optional

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

from core.config import settings
from core.database.models.message import MessageORM
from core.database.repositories.message import MessageRepository
from . import logger


class MessageParser:
    def __init__(self):
        self.CLIENT: TelegramClient = TelegramClient(
            settings.SESSION_NAME, settings.API_ID, settings.API_HASH
        )

    async def _store_message(self, message: Message) -> None:
       if getattr(message, "from_id", None) is None or not hasattr(message.from_id, "user_id"):
           return
       async with MessageRepository() as repo:
           await repo.add_message(MessageORM(
               message_id=message.id,
               message_text=message.message,
               message_date=message.date,
               from_chat_id=message.chat_id,
               from_user_id=message.from_id.user_id,
               embedding=None
           ))

    def setup_event_handler(self) -> None:
        @self.CLIENT.on(events.NewMessage(chats=settings.CHAT_ID))
        async def _(event: events.NewMessage.Event) -> None:
            await self._store_message(event.message)

    async def sync_messages(
        self,
        reverse: bool = True,
    ) -> None:
        await self.CLIENT.start()

        try:
            await self.CLIENT.get_entity(settings.CHAT_ID)
        except ValueError:
            await self.CLIENT.get_dialogs()

        async for msg in self.CLIENT.iter_messages(
            entity=settings.CHAT_ID,
            reverse=True,
        ):
            await self._store_message(msg)

        self.setup_event_handler()

        logger.info("Listening for new messages…")
        await self.CLIENT.run_until_disconnected()
