from fastapi import APIRouter

from .users import auth_router, user_router
from .forms import forms_router
from .forms.reviews import reviews_router

main_router: APIRouter = APIRouter(prefix='/api')

main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(forms_router)
main_router.include_router(reviews_router)
