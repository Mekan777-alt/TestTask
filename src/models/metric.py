from typing import List, TYPE_CHECKING
from datetime import datetime

from database.base import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime, func

if TYPE_CHECKING:
    from models import MetricRecord
    from models import User


class Metric(Base):
    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    records: Mapped[List["MetricRecord"]] = relationship(back_populates="metric", cascade="all, delete-orphan")
    owner: Mapped["User"] = relationship(back_populates="metrics")

