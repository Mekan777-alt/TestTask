from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from api.controllers.auth_controller import router as auth_router
from api.controllers.metric_controller import router as metric_controller
from api.controllers.tag_controller import router as tag_controller
from core.config import settings
from database.redis import close_redis_client, get_redis_client
from middlewares.cors import add_cors_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.redis.url, decode_responses=False)

    FastAPICache.init(RedisBackend(redis), prefix="cache")

    await get_redis_client()
    yield
    await redis.close()
    await close_redis_client()


def create_app() -> FastAPI:
    app = FastAPI(
        title="API",
        debug=True,
        root_path="/api",
        lifespan=lifespan
    )

    add_cors_middleware(app)

    app.include_router(auth_router)
    app.include_router(metric_controller)
    app.include_router(tag_controller)

    return app

app = create_app()
