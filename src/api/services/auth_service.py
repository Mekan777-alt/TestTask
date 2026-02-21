from datetime import datetime, timezone

from fastapi import Depends, HTTPException
from starlette import status

from api.dto.auth_dto import AuthRequestDTO, AuthResponseDTO, RefreshRequestDTO, LogoutRequestDTO, MessageResponseDTO
from api.repositories.auth_repository import AuthRepository, get_auth_repository
from api.services.blacklist_service import BlackListService, get_blacklist_service
from core.security import verify_password, create_access_token, create_refresh_token, decode_token
from core.config import settings
from models import UserStatus


class AuthService:
    def __init__(self, auth_repository: AuthRepository, blacklist_service: BlackListService):
        self.auth_repository = auth_repository
        self.blacklist_service = blacklist_service

    async def login_service(self, data: AuthRequestDTO) -> AuthResponseDTO:
        user = await self.auth_repository.get_user_by_email(str(data.email))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с почтой {data.email} не найден"
            )

        if not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный пароль"

            )

        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Данный пользователь не активен"
            )

        user.last_login = datetime.now(timezone.utc)
        await self.auth_repository.update(user)

        access_token = create_access_token(user_id=str(user.id), email=user.email)
        refresh_token = create_refresh_token(user_id=str(user.id))

        return AuthResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.jwt.access_expire_minutes * 60
        )

    async def refresh_token_service(self, data: RefreshRequestDTO):
        payload = decode_token(data.refresh_token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный refresh токен"
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный тип токена"
            )

        jti = str(payload.get("jti"))
        if await self.blacklist_service.is_blacklisted(jti, "refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Токен отозван"
            )

        user_id = payload.get("sub")
        user = await self.auth_repository.get_by_id(int(user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден"
            )

        if user.status != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт заблокирован"
            )

        exp = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        await self.blacklist_service.add_to_blacklist(jti, "refresh", exp)

        access_token = create_access_token(str(user.id), user.role.name)
        refresh_token = create_refresh_token(str(user.id))

        return AuthResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.jwt.access_expire_minutes * 60
        )

    async def logout_service(self, data: LogoutRequestDTO):
        refresh_payload = decode_token(data.refresh_token)

        if not refresh_payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный refresh токен"
            )

        if refresh_payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный тип токена"
            )

        await self.blacklist_service.add_to_blacklist(
            token_type=refresh_payload.get("type"),
            jti=refresh_payload.get("jti"),
            expires_at=datetime.fromtimestamp(refresh_payload.get("exp"), tz=timezone.utc)
        )

        return MessageResponseDTO(message="Успешный выход из системы")

def get_auth_service(
    auth_repository: AuthRepository = Depends(get_auth_repository),
    blacklist_service: BlackListService = Depends(get_blacklist_service)
) -> AuthService:
    return AuthService(auth_repository, blacklist_service)