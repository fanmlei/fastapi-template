import redis.asyncio as aioredis
from fastapi import HTTPException
from loguru import logger

from src.core.config import settings


class RedisManager:
    """缓存."""

    def __init__(self) -> None:
        self.redis_url: str = settings.REDIS_URL
        self.redis_client: aioredis.Redis | None = None

    async def init_redis(self, max_connections: int = 10, decode_responses: bool = True) -> None:
        """初始化Redis连接池
        :param redis_url: Redis连接地址
        :param max_connections: 最大连接数
        :return: None.
        """
        logger.info(f"Initializing Redis connection pool with {max_connections} connections.")
        self.redis_client = aioredis.Redis.from_url(
            self.redis_url, max_connections=max_connections, decode_responses=decode_responses
        )
        logger.info("Redis connection pool initialized.")

    async def close_redis(self) -> None:
        """
        关闭Redis连接池
        :return: None.
        """
        if self.redis_client is not None:
            await self.redis_client.aclose()
            self.redis_client = None
        logger.info("Redis connection pool closed.")

    async def get_client(self) -> aioredis.Redis:
        """
        获取 Redis 客户端实例。
        在使用此方法之前，请确保连接池已通过 `init_redis` 初始化。
        """
        if self.redis_client is None:
            raise RuntimeError("Redis连接池未初始化")
        return self.redis_client


redis_manager = RedisManager()


async def get_redis() -> aioredis.Redis:
    """
    FastAPI 依赖项，用于获取已初始化的 Redis 客户端。
    """
    try:
        return await redis_manager.get_client()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=f"Redis 服务未初始化或不可用: {e}") from e
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"无法获取 Redis 连接: {e}") from e
