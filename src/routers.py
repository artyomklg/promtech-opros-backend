from fastapi import APIRouter

# , reset_password_roter, verify_router, oauth_router
from .auth import auth_router, user_router
from .forms import forms_router
from .reviews import reviews_router


main_router: APIRouter = APIRouter(prefix='/api')

main_router.include_router(auth_router)

main_router.include_router(user_router)

main_router.include_router(forms_router)

main_router.include_router(resp_router)
