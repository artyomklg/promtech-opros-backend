from fastapi import APIRouter, Depends, HTTPException, status

from ..database import get_async_session, AsyncSession
from ..auth.schemas import User
from ..auth.dependencies import get_current_user, get_current_superuser
from .schemas import Review

reviews_router: APIRouter = APIRouter(prefix='/forms', tags=["reviews"])


@reviews_router.post('/{form_id}/reviews/')
async def post_review(
    form_id: int,
    review: Review,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    return


@reviews_router.get('/{form_id}/reviews/{review_id}')
async def get_review(
    form_id: int,
    review_id: int,
    user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    return


@reviews_router.get('/{form_id}/reviews/')
async def get_reviews(
    form_id: int,
    user: User = Depends(get_current_superuser),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    return
