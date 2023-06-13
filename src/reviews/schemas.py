import uuid

from pydantic import BaseModel


class ChoisePrompt(BaseModel):
    option: list[int] = []


class TextPrompt(BaseModel):
    placeholder: str

class Answer(BaseModel):
    item_id: int
    prompt: ChoisePrompt | TextPrompt


class Review(BaseModel):
    answers: list[Answer] = []
