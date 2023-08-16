import uuid
from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class ChoisePrompt(BaseModel):
    options: Optional[List[int]] = []


class TextPrompt(BaseModel):
    placeholder: str


class AnswerBase(BaseModel):
    promt: Optional[Union[ChoisePrompt, TextPrompt]] = None


class AnswerCreate(AnswerBase):
    item_id: int


class AnswerUpdate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    item_id: int
    review_id: int
    prompt: ChoisePrompt | TextPrompt

    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    pass


class ReviewCreate(ReviewBase):
    form_id: int
    user_id: uuid.UUID


class ReviewUpdate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    form_id: int
    user_id: uuid.UUID
    review_time: datetime
    answers: List[Answer] = []

    model_config = ConfigDict(from_attributes=True)
