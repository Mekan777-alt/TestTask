from typing import List

from api.services.metric_service import MetricService, get_metric_service
from starlette import status
from fastapi import Depends, APIRouter
from api.dto.metric_dto import MetricRequestDTO, MetricResponseDTO
from core.dependencies import CurrentUser


router = APIRouter(
    prefix="/v1/metrics",
    tags=["Работа с метриками"],
)



@router.post(
    path="",
    summary="Создание метрик",
    status_code=status.HTTP_201_CREATED,
    response_model=MetricResponseDTO
)
async def create_metric(
        data: MetricRequestDTO,
        current_user: CurrentUser,
        service: MetricService = Depends(get_metric_service),
):
    return await service.create_metric_service(data, current_user)


@router.get(
    path="",
    summary="Возвращает массив метрик пользователя",
    status_code=status.HTTP_200_OK,
    response_model=List[MetricResponseDTO]
)
async def get_metrics(current_user: CurrentUser,service: MetricService = Depends(get_metric_service)):
    return await service.get_metrics_service(current_user)
