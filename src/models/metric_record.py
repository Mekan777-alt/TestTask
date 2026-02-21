from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from models.metric import Metric
    from models.tag import Tag

metric_record_tags = Table(
    "metric_record_tags",
    Base.metadata,
    Column("record_id", ForeignKey("metric_records.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class MetricRecord(Base):
    __tablename__ = "metric_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    metric_id: Mapped[int] = mapped_column(ForeignKey("metrics.id", ondelete="CASCADE"))
    value: Mapped[Decimal] = mapped_column(Numeric(20, 4))
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    metric: Mapped["Metric"] = relationship(back_populates="records")
    tags: Mapped[List["Tag"]] = relationship(secondary=metric_record_tags)
