from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import Base


class MessageORM(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, primary_key=True
    )
    message_text: Mapped[str] = mapped_column(String, nullable=True)
    message_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    from_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    from_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    embedding: Mapped[list[float]] = mapped_column(Vector(1024), nullable=True)

    # TODO: add media support in *** format

    repr_cols_num: int = 7
