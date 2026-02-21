from typing import List

from fastapi import HTTPException, Depends
from fastapi_cache import FastAPICache
from starlette import status

from models import User, Metric, MetricRecord
from api.dto.metric_dto import MetricRequestDTO, MetricRecordRequestDTO
from api.repositories.metric_repository import MetricRepository, get_metric_repository
from api.repositories.tag_repository import TagRepository, get_tag_repository


class MetricService:
    def __init__(self, metric_repository: MetricRepository, tag_repository: TagRepository):
        self.metric_repository = metric_repository
        self.tag_repository = tag_repository

    def _cache_key(self, user_id: int, metric_id: int) -> str:
        return f"cache:records:{user_id}:{metric_id}"

    async def create_metric_service(self, data: MetricRequestDTO, current_user: User) -> Metric:
        metric = Metric(
            name=data.name,
            description=data.description or "",
            owner_id=current_user.id,
        )
        return await self.metric_repository.create(metric)

    async def get_metrics_service(self, current_user: User) -> List[Metric]:
        return await self.metric_repository.get_metrics_by_owner_id(current_user.id)

    async def get_metric_records_service(self, metric_id: int, current_user: User) -> List[MetricRecord]:
        metric = await self.metric_repository.get_metric_by_id_and_owner(metric_id, current_user.id)

        if not metric:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Метрика с id={metric_id} не найдена"
            )

        return await self.metric_repository.get_records_by_metric_id(metric_id, current_user.id)

    async def get_metric_record_by_id_service(self, metric_id: int, record_id: int, current_user: User) -> MetricRecord:
        record = await self.metric_repository.get_record_by_id(metric_id, record_id, current_user.id)

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Запись с id={record_id} не найдена в метрике с id={metric_id}"
            )

        return record

    async def create_metric_record_service(
            self,
            metric_id: int,
            data: MetricRecordRequestDTO,
            current_user: User
    ) -> MetricRecord:
        metric = await self.metric_repository.get_metric_by_id_and_owner(metric_id, current_user.id)

        if not metric:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Метрика с id={metric_id} не найдена"
            )

        tags = []
        if data.tag_ids:
            tags = await self.tag_repository.get_tags_by_ids(data.tag_ids)

            if len(tags) != len(data.tag_ids):
                found_ids = {tag.id for tag in tags}
                missing_tag_ids = set(data.tag_ids) - found_ids
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Теги с id={missing_tag_ids} не найдены"
                )

        record = MetricRecord(
            metric_id=metric_id,
            value=data.value,
            timestamp=data.timestamp,
            tags=tags,
        )

        record = await self.metric_repository.create_record(record)
        await FastAPICache.get_backend().clear(key=self._cache_key(current_user.id, metric_id))

        return record


def get_metric_service(
        metric_repository: MetricRepository = Depends(get_metric_repository),
        tag_repository: TagRepository = Depends(get_tag_repository),
) -> MetricService:
    return MetricService(metric_repository, tag_repository)
