from telethon import TelegramClient

from core.config import settings


class TGClient:
    def __init__(self) -> None:
        self.client = TelegramClient(
            settings.SESSION_NAME, settings.API_ID, settings.API_HASH
        )

    async def start(self) -> None:
        await self.client.start()

    async def get_entity_safe(self, chat_id: int):
        try:
            return await self.client.get_entity(chat_id)
        except ValueError:
            return await self.client.get_dialogs()

    async def run_forever(self):
        await self.client.run_until_disconnected()
