import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from .models import Review as ReviewModel, Answer as AnswerModel
from .schemas import Review, Answer, TextPrompt, ChoisePrompt


class ReviewService:
    @classmethod
    async def create_review(cls, review: Review):
        pass

    @classmethod
    async def get_review(cls, review_id: int):
        pass

    @classmethod
    async def get_list_review(cls, form_id: int):
        pass
