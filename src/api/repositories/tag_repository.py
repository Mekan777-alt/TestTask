from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Tag
from database.base import BaseRepository
from database.session import get_session


class TagRepository(BaseRepository[Tag]):
    def __init__(self, session: AsyncSession):
        super().__init__(Tag, session)

    async def get_tags_by_ids(self, tag_ids: List[int]) -> List[Tag]:
        result = await self.session.execute(
            select(Tag).where(Tag.id.in_(tag_ids))
        )
        return list(result.scalars().all())

def get_tag_repository(session: AsyncSession = Depends(get_session)) -> TagRepository:
    return TagRepository(session)