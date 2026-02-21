from contextlib import asynccontextmanager
from core.config import settings
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi import FastAPI
from database.redis import close_redis_client, get_redis_client
from api.controllers.auth_controller import router as auth_router
from api.controllers.metric_controller import router as metric_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = f"redis://:{settings.redis.password}@{settings.redis.host}:{settings.redis.port}/{settings.redis.db}"
    redis = aioredis.from_url(redis_url, decode_responses=False)

    FastAPICache.init(RedisBackend(redis), prefix="cache")

    await get_redis_client()
    yield
    await redis.close()
    await close_redis_client()


def create_app() -> FastAPI:
    app = FastAPI(
        title="API",
        debug=True,
        lifespan=lifespan
    )

    app.include_router(auth_router)
    app.include_router(metric_controller)

    return app

app = create_app()
