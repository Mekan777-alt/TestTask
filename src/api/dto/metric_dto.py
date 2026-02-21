from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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