import uuid

from pydantic import BaseModel


class ChoisePrompt(BaseModel):
    option: list[int] = []


class TextPrompt(BaseModel):
    placeholder: str

class AnswerCreate(BaseModel):
    item_id: int
    prompt: ChoisePrompt | TextPrompt


class ReviewCreate(BaseModel):
    answers: list[AnswerCreate] = []
