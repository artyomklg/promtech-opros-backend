from fastapi import APIRouter

from .auth import auth_router, register_router, users_roter  # , reset_password_roter, verify_router, oauth_router
from .forms import forms_router
from .responses import resp_router

# from auth import fastapi_users

main_router: APIRouter = APIRouter(prefix='/api')

main_router.include_router(
    auth_router, prefix="/auth/jwt", tags=["auth"]
)

main_router.include_router(
    register_router, prefix='/auth', tags=["auth"]
)

main_router.include_router(
    users_roter, prefix='/users', tags=["users"]
)

# main_router.include_router(
#     reset_password_roter, prefix='/auth', tags=["auth"]
# )

# main_router.include_router(
#     verify_router, prefix='/auth', tags=["auth"]
# )

# main_router.include_router(
#     oauth_router, prefix='/auth/google', tags=["auth"]
# )

main_router.include_router(forms_router)

main_router.include_router(resp_router)
