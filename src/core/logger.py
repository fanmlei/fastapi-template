import logging
import sys
from pathlib import Path

from loguru import logger

from src.core.config import settings


class InterceptHandler(logging.Handler):
    """这个处理器会拦截标准的 logging 模块的日志记录"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # type: ignore
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_logger() -> None:
    logger.remove()

    LOG_LEVEL = settings.LOG_LEVEL

    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        enqueue=True,
    )

    log_file_path = Path(settings.LOG_FILE_PATH)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_file_path,
        level=LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="100 MB",
        retention="7 days",
        compression="zip",
        enqueue=True,
        serialize=False,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    for uvicorn_logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access", "uvicorn.asgi", "tortoise"]:
        uvicorn_logger = logging.getLogger(uvicorn_logger_name)
        uvicorn_logger.handlers = [InterceptHandler()]
        uvicorn_logger.propagate = False

    logger.info("Loguru logging setup complete.")
