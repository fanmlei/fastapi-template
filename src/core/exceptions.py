from enum import IntEnum

from fastapi import status
from fastapi.requests import Request
from loguru import logger

from .codes import BusinessResponseCode
from .response import UnifiedJSONResponse


class UnifiedException(Exception):
    def __init__(self, name: str, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> None:
        self.name = name
        self.code = BusinessResponseCode.FAILED
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

async def unified_exception_handler(request: Request, exc: UnifiedException) -> UnifiedJSONResponse:
    logger.error(f"BusinessException caught: {exc.message}, code: {exc.code.value if isinstance(exc.code, IntEnum) else exc.code}", exc_info=True)
    return UnifiedJSONResponse(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        data=None
    )
