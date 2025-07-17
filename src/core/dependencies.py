import jwt
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from loguru import logger

from .config import settings
from .exceptions import UnifiedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        userid: int = payload.get("userid")
        if userid is None:
            raise UnifiedException(name="token_invalid", message="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED)
    except PyJWTError as e:
        logger.error(f"JWTError caught: {e}", exc_info=True)
        raise UnifiedException(name="token_invalid", message="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED) from e
    return userid
