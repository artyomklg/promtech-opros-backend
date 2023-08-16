from fastapi import APIRouter, Depends

from ...users.dependencies import get_current_active_user, get_current_superuser
from ...users.models import UserModel
from .schemas import AnswerCreate, Review, ReviewCreate
from .service import ReviewService

reviews_router: APIRouter = APIRouter(prefix="/forms", tags=["reviews"])


@reviews_router.post("/{form_id}/reviews")  # ! Ready
async def post_review(
    form_id: int,
    answers: list[AnswerCreate],
    user: UserModel = Depends(get_current_active_user),
) -> Review:
    return await ReviewService.create_review(ReviewCreate(form_id, user.id), answers)


@reviews_router.get("/{form_id}/reviews")
async def get_reviews(
    form_id: int, user: UserModel = Depends(get_current_superuser)
) -> None:
    return


@reviews_router.get("/{form_id}/reviews/{review_id}")
async def get_review(
    form_id: int,
    review_id: int,
    user: UserModel = Depends(get_current_active_user),
) -> None:
    # ! Надо чтобы было доступно либо владельцу либо админам
    return
