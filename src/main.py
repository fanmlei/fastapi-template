from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.apps.user.routers import user_router
from src.core.config import settings
from src.core.exceptions import UnifiedException, unified_exception_handler
from src.core.logger import setup_logger
from src.core.middleware import AuthMiddleware
from src.db.cache import redis_manager
from src.db.database import init_tortoise

setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Application startup...")
    await init_tortoise(app)
    await redis_manager.init_redis()
    yield
    await redis_manager.close_redis()
    logger.info("Application shutdown...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(user_router)

app.add_exception_handler(UnifiedException, unified_exception_handler)  # type: ignore

app.add_middleware(AuthMiddleware)
