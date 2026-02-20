from datetime import datetime, timezone
from database.redis import get_redis_client
from fastapi import Depends
from redis.asyncio import Redis


class BlackListService:
    def __init__(self, client: Redis):
        self.client = client


    async def is_blacklisted(self, jti: str, token_type: str) -> bool:
        key = f"blacklist:{token_type}:{jti}"
        return await self.client.exists(key) == 1

    async def add_to_blacklist(self, jti: str, token_type: str, expires_at: datetime) -> None:
        key = f"blacklist:{token_type}:{jti}"
        ttl = int((expires_at - datetime.now(timezone.utc)).total_seconds())

        if ttl > 0:
            await self.client.setex(key, ttl, "1")


def get_blacklist_service(client: Redis = Depends(get_redis_client)):
    return BlackListService(client)