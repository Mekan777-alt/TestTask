from redis.asyncio import Redis

from core.config import settings

redis_client: Redis | None = None

async def get_redis_client() -> Redis | None:
    global redis_client

    if redis_client is None:
        redis_client = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db,
            password=settings.redis.password,
            decode_responses=True
        )

    return redis_client

async def close_redis_client() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None
