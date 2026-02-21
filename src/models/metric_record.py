from typing import List, TYPE_CHECKING

from database.base import Base
from decimal import Decimal
from sqlalchemy import func, ForeignKey, Numeric, DateTime, Table, Column
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship

if TYPE_CHECKING:
    from models.tag import Tag
    from models.metric import Metric

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