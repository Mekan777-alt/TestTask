from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import Tag
from database.base import BaseRepository
from database.session import get_session


class TagRepository(BaseRepository[Tag]):
    def __init__(self, session: AsyncSession):
        super().__init__(Tag, session)


def get_tag_repository(session: AsyncSession = Depends(get_session)) -> TagRepository:
    return TagRepository(session)