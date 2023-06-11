from typing import List

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate, Token, User
from .service import AuthService, UserService
from .dependencies import get_current_user, get_current_superuser
from .exceptions import InvalidCredentialsException
from ..database import get_async_session


auth_router = APIRouter(prefix="/auth", tags=["auth"])


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
        max_age=3600,
        secure=True,
        httponly=True,
        samesite='lax',
    )
    response.set_cookie(
        'refresh_token',
        token.refresh_token,
        max_age=60 * 60 * 24 * 30,
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
    response.set_cookie(
        'access_token',
        '',
        max_age=0,
        secure=True,
        httponly=True,
        samesite='lax',
    )
    response.set_cookie(
        'refresh_token',
        '',
        max_age=0,
        secure=True,
        httponly=True,
        samesite='lax',
    )
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
        max_age=3600,
        secure=True,
        httponly=True,
        samesite='lax',
    )
    response.set_cookie(
        'refresh_token',
        new_token.refresh_token,
        max_age=60 * 60 * 24 * 30,
        secure=True,
        httponly=True,
        samesite='lax',
    )
    return new_token


user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get("/me", response_model=User)
async def get_current_user_route(
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


@user_router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, current_user: User = Depends(get_current_superuser), session: AsyncSession = Depends(get_async_session), service: UserService = Depends()):
    return await service.get_user(user_id, session)


@user_router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User, current_user: User = Depends(get_current_superuser), session: AsyncSession = Depends(get_async_session), service: UserService = Depends()):
    return await service.update_user(user_id, user, session)


@user_router.delete("/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_current_superuser), session: AsyncSession = Depends(get_async_session), service: UserService = Depends()):
    await service.delete_user(user_id, session)