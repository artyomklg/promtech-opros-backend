from fastapi import APIRouter

from .base_config import fastapi_users, auth_backend  # , google_oauth_client
from .schemas import UserCreate, UserRead, UserUpdate
from ..config import settings

auth_router: APIRouter = fastapi_users.get_auth_router(auth_backend)

register_router: APIRouter = fastapi_users.get_register_router(
    UserRead, UserCreate)

# reset_password_roter: APIRouter = fastapi_users.get_reset_password_router()

# verify_router: APIRouter = fastapi_users.get_verify_router(UserRead)

users_roter: APIRouter = fastapi_users.get_users_router(UserRead, UserUpdate)

# oauth_router: APIRouter = fastapi_users.get_oauth_router(
#     google_oauth_client, auth_backend, settings.SECRET)
