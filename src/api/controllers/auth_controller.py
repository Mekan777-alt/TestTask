from fastapi import Depends, APIRouter
from starlette import status
from api.services.auth_service import get_auth_service, AuthService
from core.dependencies import CurrentUser
from api.dto.auth_dto import AuthRequestDTO, AuthResponseDTO, RefreshRequestDTO, MessageResponseDTO, LogoutRequestDTO, \
    UserResponseDTO

router = APIRouter(
    prefix="/v1/auth",
    tags=["Авторизация пользователей"]
)


@router.post(
    path="/token",
    summary="Авторизация пользователя",
    status_code=status.HTTP_200_OK,
    response_model=AuthResponseDTO
)
async def login(data: AuthRequestDTO, service: AuthService = Depends(get_auth_service)):
    return await service.login_service(data)


@router.post(
    path="/refresh",
    summary="Обновление токенов",
    status_code=status.HTTP_200_OK,
    response_model=AuthResponseDTO
)
async def refresh_token(
        data: RefreshRequestDTO,
        current_user: CurrentUser,
        service: AuthService = Depends(get_auth_service)
):
    return await service.refresh_token_service(data)

@router.post(
    path="/logout",
    summary="Выход из системы",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseDTO,
)
async def logout(data: LogoutRequestDTO, current_user: CurrentUser, service: AuthService = Depends(get_auth_service)):
    return await service.logout_service(data)

@router.get(
    path="/me",
    summary="Данные о себе",
    response_model=UserResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def me(current_user: CurrentUser):
    return current_user