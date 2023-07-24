from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ReviewModel, AnswerModel
from .schemas import (
    AnswerCreate, AnswerUpdate,
    ReviewCreate, ReviewUpdate
)
from ...dao import BaseDAO


class ReviewDAO(BaseDAO[ReviewModel, AnswerCreate, AnswerUpdate]):
    model = ReviewModel


class AnswerDao(BaseDAO[AnswerModel, ReviewCreate, ReviewUpdate]):
    model = AnswerModel
