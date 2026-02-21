from pydantic import BaseModel, Field


class TagResponseDTO(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор", examples=[1, 2])
    name: str = Field(..., description="Название тэга")
