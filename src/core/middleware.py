import jwt
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from .config import settings
from .model import current_user_id


async def get_jwt_payload(request: Request) -> dict | None:
    """
    获取jwt payload
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer "):]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.exceptions.DecodeError:
            return None
        else:
            return payload
    return None


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        payload = await get_jwt_payload(request)
        user_id = payload.get("user_id") if payload else None
        token = current_user_id.set(user_id)
        try:
            response = await call_next(request)
        finally:
            current_user_id.reset(token)
        return response
