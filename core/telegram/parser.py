from typing import Any, Dict, Optional

from telethon import TelegramClient, events

from core.config import settings
from core.database.repositories.message import MessageRepository
from . import logger


class MessageParser:
    def __init__(self):
        self.CLIENT: TelegramClient = TelegramClient(
            settings.SESSION_NAME, settings.API_ID, settings.API_HASH
        )

    async def _store_message(self, event: events.NewMessage.Event) -> None:
       pass

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
