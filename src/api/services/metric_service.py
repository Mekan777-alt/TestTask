from typing import List

from fastapi import HTTPException, Depends
from starlette import status
from models import User, Metric
from api.dto.metric_dto import MetricRequestDTO, MetricResponseDTO
from api.repositories.metric_repository import MetricRepository, get_metric_repository


class MetricService:
    def __init__(self, metric_repository: MetricRepository):
        self.metric_repository = metric_repository

    async def create_metric_service(self, data: MetricRequestDTO, current_user: User):

        metric = Metric(
            name=data.name,
            description=data.description or "",
            owner_id=current_user.id,
        )

        return await self.metric_repository.create(metric)


    async def get_metrics_service(self, current_user: User):
        return await self.metric_repository.get_metrics_by_owner_id(current_user.id)



def get_metric_service(metric_repository: MetricRepository = Depends(get_metric_repository)):
    return MetricService(metric_repository)