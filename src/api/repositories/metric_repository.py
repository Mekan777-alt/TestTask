from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import BaseRepository
from database.session import get_session
from models import Metric

class MetricRepository(BaseRepository[Metric]):
    def __init__(self, session: AsyncSession):
        super().__init__(Metric, session)

    async def get_metrics_by_owner_id(self, owner_id: int) -> List[Metric]:
        result = await self.session.execute(
            select(Metric)
            .where(Metric.owner_id == owner_id)
        )

        return list(result.scalars().all())

def get_metric_repository(session: AsyncSession = Depends(get_session)):
    return MetricRepository(session)