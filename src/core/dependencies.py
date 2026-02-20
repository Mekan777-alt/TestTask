from fastapi import Depends, HTTPException
from sqlalchemy import select
from starlette import status
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from api.services.blacklist_service import BlackListService, get_blacklist_service
from core.security import decode_token
from models import User, UserStatus

bearer_scheme = HTTPBearer()


async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
        session: Annotated[AsyncSession, Depends(get_session)],
        blacklist: Annotated[BlackListService, Depends(get_blacklist_service)]
) -> User:

    token = credentials.credentials

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный тип токена"
        )

    jti = payload.get("jti")

    if await blacklist.is_blacklisted(jti, "access"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Токен аннулирован"
        )

    user_id = payload.get("sub")
    result = await session.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )

    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен или заблокирован"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

