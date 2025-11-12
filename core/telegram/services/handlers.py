from telethon import events
from telethon.tl.custom.message import Message

from core.telegram.services.message import MessageService


class EventHandler:
    def __init__(self, client, service: MessageService):
        self.client = client
        self.service = service

    def setup_new_message_listener(self, chat_id: int) -> None:
        @self.client.on(events.NewMessage(chats=chat_id))
        async def _(event: events.NewMessage.Event):
            message: Message = event.message

            if not message.message or message.media:
                return None

            await self.service.store_message(message)
