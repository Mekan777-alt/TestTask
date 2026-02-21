from typing import List

from fastapi import APIRouter, Depends, Path
from fastapi_cache.decorator import cache
from starlette import status

from api.dto.metric_dto import MetricRecordRequestDTO, MetricRecordResponseDTO, MetricRequestDTO, MetricResponseDTO
from api.services.metric_service import MetricService, get_metric_service
from core.cache_utils import records_cache_key
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
async def get_metrics(current_user: CurrentUser, service: MetricService = Depends(get_metric_service)):
    return await service.get_metrics_service(current_user)


@router.get(
    path="/{metric_id}/records",
    summary="Список записей конкретной метрики",
    status_code=status.HTTP_200_OK,
    response_model=List[MetricRecordResponseDTO]
)
@cache(expire=60, key_builder=records_cache_key)
async def get_metric_records(
        metric_id: int,
        current_user: CurrentUser,
        service: MetricService = Depends(get_metric_service)
):
    return await service.get_metric_records_service(metric_id, current_user)

@router.post(
    path="/{metric_id}/records",
    summary="Cоздание записи метрики",
    status_code=status.HTTP_201_CREATED,
    response_model=MetricRecordResponseDTO
)
async def create_metric_record(
        data: MetricRecordRequestDTO,
        current_user: CurrentUser,
        metric_id: int = Path(..., description="ID метрики"),
        service: MetricService = Depends(get_metric_service)
):
    return await service.create_metric_record_service(metric_id, data, current_user)

@router.get(
    path="/{metric_id}/records/{record_id}",
    summary="Детализация одной записи метрики",
    status_code=status.HTTP_200_OK,
    response_model=MetricRecordResponseDTO
)
async def get_metric_record(
        current_user: CurrentUser,
        metric_id: int = Path(..., gt=0, description="ID метрики"),
        record_id: int = Path(..., gt=0, description="ID записи"),
        service: MetricService = Depends(get_metric_service)
):
    return await service.get_metric_record_by_id_service(metric_id, record_id, current_user)
