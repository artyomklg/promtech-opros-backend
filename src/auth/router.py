from typing import List

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate, Token, User
from .service import AuthService, UserService
from .dependencies import get_current_user, get_current_superuser
from .exceptions import InvalidCredentialsException
from ..database import get_async_session
from ..config import settings


auth_router = APIRouter(prefix="/auth", tags=["auth"])
user_router = APIRouter(prefix="/users", tags=["user"])


@auth_router.post("/register", response_model=User)
async def register(
    user: UserCreate,
    service: UserService = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    return await service.register_new_user(user, session)


@auth_router.post("/login")
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends()
):
    user = await service.authenticate_user(credentials.username, credentials.password, session)
    if not user:
        raise InvalidCredentialsException
    token = await service.create_token(user, session)
    response.set_cookie(
        'access_token',
        token.access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        httponly=True,
        samesite='lax',
    )
    response.set_cookie(
        'refresh_token',
        token.refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
        secure=True,
        httponly=True,
        samesite='lax',
    )
    return {"access_token": token.access_token, "token_type": "bearer"}


@auth_router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
    service: AuthService = Depends()
):
    response.set_cookie('access_token', '', max_age=0)
    response.set_cookie('refresh_token', '', max_age=0)

    await service.logout(request.cookies.get('refresh_token'), session)
    return {"message": "Logged out successfully"}


@auth_router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    service: AuthService = Depends()
):
    refresh_token = request.cookies.get("refresh_token")
    new_token = await service.refresh_token(refresh_token, session)
    response.set_cookie(
        'access_token',
        new_token.access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        httponly=True,
        samesite='lax',
    )
    response.set_cookie(
        'refresh_token',
        new_token.refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
        secure=True,
        httponly=True,
        samesite='lax',
    )
    return new_token


@auth_router.post("/abort")
async def abort_all_sessions(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
    service: AuthService = Depends()
):
    response.set_cookie('access_token', '', max_age=0)
    response.set_cookie('refresh_token', '', max_age=0)

    await service.abort_all_sessions(user.id, session)
    return {"message": "All sessions was aborted"}


@user_router.get("", response_model=list[User])
async def get_users_list(
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session),
    service: UserService = Depends()
):
    return await service.get_users_list(session)


@user_router.get("/me", response_model=User)
async def get_current_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    service: UserService = Depends()
):
    return await service.get_user(current_user.id, session)


@user_router.put("/me", response_model=User)
async def update_current_user(
    user: User,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    service: UserService = Depends()
):
    return await service.update_user(current_user.id, user, session)


@user_router.delete("/me", response_model=User)
async def delete_current_user(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    user_service: UserService = Depends(),
    auth_service: AuthService = Depends()
):
    response.set_cookie('access_token', '', max_age=0)
    response.set_cookie('refresh_token', '', max_age=0)

    await auth_service.logout(request.cookies.get('refresh_token'), session)
    return await user_service.delete_user(current_user.id, session)


@user_router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session),
    service: UserService = Depends()
):
    return await service.get_user(user_id, session)


@user_router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user: User,
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session),
    service: UserService = Depends()
):
    return await service.update_user_from_superuser(user_id, user, session)


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session),
    service: UserService = Depends()
):
    await service.delete_user(user_id, session)
