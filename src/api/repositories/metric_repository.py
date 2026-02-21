from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import BaseRepository
from database.session import get_session
from models import Metric, MetricRecord


class MetricRepository(BaseRepository[Metric]):
    def __init__(self, session: AsyncSession):
        super().__init__(Metric, session)

    async def get_metrics_by_owner_id(self, owner_id: int) -> List[Metric]:
        result = await self.session.execute(
            select(Metric)
            .where(Metric.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def get_records_by_metric_id(self, metric_id: int, owner_id: int) -> List[MetricRecord]:
        result = await self.session.execute(
            select(Metric)
            .options(
                selectinload(Metric.records)
                .selectinload(MetricRecord.tags)
            )
            .where(
                Metric.id == metric_id,
                Metric.owner_id == owner_id,
            )
        )
        metric = result.scalar_one_or_none()

        if metric is None:
            return []
        return metric.records

    async def get_record_by_id(self, metric_id: int, record_id: int, owner_id: int) -> Optional[MetricRecord]:
        result = await self.session.execute(
            select(MetricRecord)
            .join(Metric)
            .options(selectinload(MetricRecord.tags))
            .where(
                MetricRecord.id == record_id,
                MetricRecord.metric_id == metric_id,
                Metric.owner_id == owner_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_metric_by_id_and_owner(self, metric_id: int, owner_id: int) -> Optional[Metric]:
        result = await self.session.execute(
            select(Metric).where(
                Metric.id == metric_id,
                Metric.owner_id == owner_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_record(self, model: MetricRecord) -> MetricRecord:
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model, attribute_names=["tags"])
        return model


def get_metric_repository(session: AsyncSession = Depends(get_session)) -> MetricRepository:
    return MetricRepository(session)
