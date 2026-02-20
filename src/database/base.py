from sqlalchemy.orm import DeclarativeBase
from typing import Generic, TypeVar, Type, List
from sqlalchemy.ext.asyncio import AsyncSession

class Base(DeclarativeBase):
    pass

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: int) -> ModelType:
        return await self.session.get(self.model, id)

    async def get_all(self) -> List[ModelType]:
        result = await self.session.execute(self.model)
        return list(result.scalars().all())

    async def create(self, model: ModelType) -> ModelType:
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model

    async def delete(self, model: ModelType) -> None:
        await self.session.delete(model)
        await self.session.flush()

    async def update(self, model: ModelType) -> ModelType:
        merged = await self.session.merge(model)
        await self.session.flush()
        await self.session.refresh(merged)
        return merged
