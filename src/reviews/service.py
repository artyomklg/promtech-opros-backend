import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from .models import Review as ReviewModel, Answer as AnswerModel
from .schemas import Review, Answer, TextPrompt, ChoisePrompt


async def create_review(
        review: Review,
        session: AsyncSession
):
    ...


async def get_review(
        review_id: int,
        session: AsyncSession
):
    ...


async def get_list_review(
        form_id: int
):
    ...
