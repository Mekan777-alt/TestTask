from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, DateTime, func, Enum as SAEnum, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.base import Base
from models.enums import UserStatus

if TYPE_CHECKING:
    from models.metric import Metric


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[UserStatus] = mapped_column(SAEnum(UserStatus), default=UserStatus.ACTIVE, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    metrics: Mapped[List["Metric"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
