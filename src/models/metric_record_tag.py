from database.base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey


class MetricRecordTag(Base):
    __tablename__ = "metric_record_tags"

    record_id: Mapped[int] = mapped_column(ForeignKey("metric_records.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
