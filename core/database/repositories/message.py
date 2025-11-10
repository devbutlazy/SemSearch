from typing import Self, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.database import engine
from core.database.models.message import MessageORM
from core.database.repositories.base import BaseRepository


class MessageRepository(BaseRepository):
    def __init__(self) -> None:
        self.session: async_sessionmaker

    async def __aenter__(self: Self) -> Self:
        self.session: async_sessionmaker = async_sessionmaker(engine)
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:  # noqa
        return await self.session().close()

    async def add_message(self, message: MessageORM) -> Optional[MessageORM]:
        """
        Add one message model to database.

        :param message: MessageORM
        :return: MessageORM if success, else None
        """
        async with self.session() as session:
            session.add(message)
            try:
                await session.commit()
                await session.refresh(message)
            except IntegrityError:
                await session.rollback()
                return None

            return message

    async def add_messages_bulk(self, messages: list[MessageORM]) -> None:
        """
        Add one message model to database.

        :param message: MessageORM
        :return: MessageORM if success, else None
        """
        async with self.session() as session:
            session.add_all(messages)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                return None

            return messages
