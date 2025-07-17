from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from src.core.config import settings

TORTOISE_ORM_CONFIG = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["apps.user.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}


async def init_tortoise(app: FastAPI) -> None:
    """初始化 TortoiseORM 并注册到 FastAPI 应用."""
    logger.info("Initializing TortoiseORM startup.")
    register_tortoise(
        app,
        config=TORTOISE_ORM_CONFIG,
        add_exception_handlers=True,
    )
    logger.info("Initializing TortoiseORM complete.")


async def close_tortoise_orm() -> None:
    """手动关闭 TortoiseORM 连接。在lifespan里面 register_tortoise 会自动关闭连接无需显式关闭."""
    await Tortoise.close_connections()
    logger.info("Closing TortoiseORM complete.")
