from pydantic import BaseModel, Field


class TagResponseDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор тега", examples=[1])
    name: str = Field(..., description="Название тега", examples=["пиковый"])

    model_config = {"from_attributes": True}
