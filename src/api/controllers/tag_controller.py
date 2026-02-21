from typing import List

from fastapi import APIRouter, Depends
from starlette import status
from api.services.tag_service import get_tag_service, TagService
from core.dependencies import CurrentUser
from api.dto.tag_dto import TagResponseDTO


router = APIRouter(
    prefix="/v1/tags",
    tags=["Работа с тегами"]
)

@router.get(
    "",
    summary="Получение списка тэгов пользователя",
    response_model=List[TagResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_tags(current_user: CurrentUser, service: TagService = Depends(get_tag_service)):
    return await service.get_tags_service()