from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.session import get_session
from database.base import BaseRepository
from models import User


class AuthRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User)
            .where(User.email == email)
        )
        return result.scalar_one_or_none()


def get_auth_repository(session: AsyncSession = Depends(get_session)) -> AuthRepository:
    return AuthRepository(session)
