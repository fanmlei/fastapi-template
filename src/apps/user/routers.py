from fastapi import APIRouter

from src.core.response import UnifiedJSONResponse

from .forms import UserLoginForm
from .service import user_login

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/login", summary="用户登录")
async def login(form: UserLoginForm) -> UnifiedJSONResponse:
    user = await user_login(form)
    return UnifiedJSONResponse(message="登录成功", data=user)
