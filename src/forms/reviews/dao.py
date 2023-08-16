from ...dao import BaseDAO
from .models import AnswerModel, ReviewModel
from .schemas import AnswerCreate, AnswerUpdate, ReviewCreate, ReviewUpdate


class ReviewDAO(BaseDAO[ReviewModel, ReviewCreate, ReviewUpdate]):
    model = ReviewModel


class AnswerDao(BaseDAO[AnswerModel, AnswerCreate, AnswerUpdate]):
    model = AnswerModel
