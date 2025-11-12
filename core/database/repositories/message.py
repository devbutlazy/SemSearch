from typing import Self, Optional

from sqlalchemy import select, func
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

    async def get_last_message_id(self) -> Optional[int]:
        """
        Get the latest (largest) message_id from the database.

        :return: int | None
        """

        async with self.session() as session:
            result = await session.execute(select(func.max(MessageORM.message_id)))
            return result.scalar_one_or_none()

    async def get_unembedded_messages(self) -> Optional[list[MessageORM]]:
        """
        Fetch all messages from the database where embedding is None.

        :return: a list of MessageORM, or None if no such messages exist.
        """

        async with self.session() as session:
            result = await session.execute(
                select(MessageORM).where(MessageORM.embedding == None)  # noqa: E711
            )
            return result.scalars().all() or None

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
