from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import User
from .exceptions import InvalidTokenException
from .utils import OAuth2PasswordBearerWithCookie
from .service import UserService
from ..database import get_async_session
from ..config import settings

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/auth/login")

async def get_current_user(
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(oauth2_scheme),
        service: UserService = Depends()
) -> Optional[User]:
    try:
        payload = jwt.decode(token,
                             settings.SECRET, algorithms=[settings.ALGORITM])
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException
    except Exception:
        raise InvalidTokenException
    return await service.get_user(user_id, session)


async def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not active")
    return current_user
