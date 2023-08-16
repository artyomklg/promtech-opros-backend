import uuid
from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from ...database import AsyncSession, async_session_maker
from .dao import AnswerDao, ReviewDAO
from .models import AnswerModel, ReviewModel
from .schemas import AnswerCreate, ReviewCreate


class ReviewService:
    @classmethod
    async def create_review(
        cls, review: ReviewCreate, answers: List[AnswerCreate]
    ) -> None:
        async with async_session_maker() as session:
            review_exist = await ReviewDAO.find_one_or_none(
                session,
                ReviewModel.form_id == review.form_id,
                ReviewModel.user_id == review.user_id,
            )
            if review_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Review alweady exist"
                )

            for answer in answers:
                if cls._is_valid_answer(session):
                    ...

            review_db = await ReviewDAO.add(session, obj_in=review)

            await session.commit()

    @classmethod
    async def get_review(cls, review_id: int):
        async with async_session_maker() as session:
            await session.commit()

    @classmethod
    async def get_list_review(cls, form_id: int):
        async with async_session_maker() as session:
            await session.commit()

    @classmethod
    async def _is_valid_answer(
        cls, session: AsyncSession, answer: AnswerCreate
    ) -> bool:
        ...
