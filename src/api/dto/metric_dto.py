from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field

from api.dto.tag_dto import TagResponseDTO


class MetricRequestDTO(BaseModel):
    name: str = Field(..., description="Название метрики", examples=["Трафик сайта"])
    description: Optional[str] = Field(None, description="Описание метрики", examples=["Количество посещений за день"])


class MetricResponseDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор", examples=[1])
    name: str = Field(..., description="Название метрики", examples=["Трафик сайта"])
    description: Optional[str] = Field(None, description="Описание метрики", examples=["Количество посещений за день"])
    owner_id: int = Field(..., description="Уникальный идентификатор пользователя", examples=[1])
    created_at: datetime = Field(..., description="Время и дата создания метрики", examples=["2026-02-20T12:00:00"])

    model_config = {"from_attributes": True}


class MetricRecordResponseDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор записи", examples=[1])
    metric_id: int = Field(..., description="ID метрики", examples=[1])
    value: float = Field(..., description="Значение показателя", examples=[1500.0])
    timestamp: datetime = Field(..., description="Время измерения", examples=["2026-02-20T10:00:00"])
    tags: List[TagResponseDTO] = Field(default=[], description="Список тегов",
                                       examples=[[{"id": 1, "name": "пиковый"}]])
    created_at: datetime = Field(..., description="Дата создания записи", examples=["2026-02-20T10:05:00"])

    model_config = {"from_attributes": True}


class MetricRecordRequestDTO(BaseModel):
    value: Decimal = Field(..., description="Значение показателя", examples=["1500.0000"])
    timestamp: datetime = Field(..., description="Время измерения", examples=["2026-02-20T10:00:00"])
    tag_ids: List[int] = Field(default=[], description="Список ID тегов", examples=[[1, 2]])
