from datetime import datetime, timezone
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.security import hash_password
from database.base import Base
from database.session import get_session
from models import Metric, Tag, User, UserStatus

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

_test_user: User | None = None


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as session:
        async with session.begin():
            yield session


async def override_get_current_user() -> User:
    return _test_user  # type: ignore[return-value]


@pytest_asyncio.fixture(autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture
async def test_user(session: AsyncSession) -> User:
    global _test_user
    user = User(
        email="test@example.com",
        password_hash=hash_password("password123"),
        status=UserStatus.ACTIVE,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    _test_user = user
    return user


@pytest_asyncio.fixture
async def test_metric(session: AsyncSession, test_user: User) -> Metric:
    metric = Metric(
        name="Тестовая метрика",
        description="Описание",
        owner_id=test_user.id,
    )
    session.add(metric)
    await session.commit()
    await session.refresh(metric)
    return metric


@pytest_asyncio.fixture
async def test_tags(session: AsyncSession) -> list[Tag]:
    tag1 = Tag(name="тег1")
    tag2 = Tag(name="тег2")
    session.add_all([tag1, tag2])
    await session.commit()
    await session.refresh(tag1)
    await session.refresh(tag2)
    return [tag1, tag2]


@pytest_asyncio.fixture
async def client(test_user: User) -> AsyncGenerator[AsyncClient, None]:
    from api_app import app
    from core.dependencies import get_current_user

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_backend = AsyncMock()
    mock_backend.clear = AsyncMock()

    with patch("api.services.metric_service.FastAPICache") as mock_cache:
        mock_cache.get_backend.return_value = mock_backend

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac

    app.dependency_overrides.clear()
