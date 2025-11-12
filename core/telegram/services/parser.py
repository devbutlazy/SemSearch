from core.config import settings
from core.telegram import logger
from core.telegram.client import TGClient
from core.telegram.services.message import MessageService
from core.telegram.services.handlers import EventHandler


class MessageParser:
    def __init__(self):
        self.client_wrapper = TGClient()
        self.service = MessageService()
        self.handler = EventHandler(self.client_wrapper.client, self.service)

    async def sync_messages(self, reverse: bool = True):
        await self.client_wrapper.start()
        await self.client_wrapper.get_entity_safe(settings.CHAT_ID)

        last_message_id = await self.service.get_last_message_id()

        async for message in self.client_wrapper.client.iter_messages(
            entity=settings.CHAT_ID, reverse=reverse, min_id=last_message_id or 0
        ):
            await self.service.store_message(message)

        logger.info("Listening for new messages…")
        self.handler.setup_new_message_listener(settings.CHAT_ID)
        await self.client_wrapper.run_forever()
