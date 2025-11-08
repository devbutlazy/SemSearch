from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import Base

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    message_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    message_text: Mapped[str] = mapped_column(String, nullable=True)
    message_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    channel_from: Mapped[str] = mapped_column(String, nullable=False)
    from_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # TODO: add media support in *** format

    repr_cols_num: int = 6
