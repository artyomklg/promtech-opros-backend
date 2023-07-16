import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .enums import ItemType, Color, Organization


class OptionBase(BaseModel):
    title: Optional[str] = None


class OptionCreate(OptionBase):
    item_id: int


class OptionUpdate(OptionBase):
    pass


class Option(OptionBase):
    id: int
    title: str
    item_id: int

    class Config():
        from_attributes = True


class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    item_type: ItemType = ItemType.ChoiceQuestion
    item_order: Optional[int] = None
    required: bool = False
    form_id: Optional[int] = None


class ItemCreate(ItemBase):
    title: str
    item_type: ItemType
    item_order: int
    required: bool
    form_id: int


class ItemUpdate(ItemBase):
    title: str
    item_type: ItemType
    item_order: int
    required: bool
    form_id: int | None
    options: list[OptionUpdate] = []

    class Config():
        from_attributes = True


class Item(ItemBase):
    id: int
    title: str
    item_type: ItemType
    item_order: int
    required: bool
    form_id: int
    options: list[Option] = []

    class Config():
        from_attributes = True


class FormBase(BaseModel):
    title: str | None = None
    description: str | None = None
    is_template: bool = False
    organization: Organization | None = Organization.OKB
    color: Color | None = Color.Orange
    created_at: datetime | None
    link: str | None
    creator_id: uuid.UUID | None = Field(
        default='a8abc8e7-c90c-48a4-bb58-bfd5e291ed66')


class FormCreate(FormBase):
    title: str
    organization: Organization
    color: Color
    link: str


class FormUpdate(FormBase):
    id: int | None
    title: str | None
    description: str | None
    is_template: bool = False
    organization: Organization
    color: Color
    link: str | None
    items: list[ItemUpdate] = []

    class Config:
        from_attributes = True


class Form(FormBase):
    id: int
    title: str
    description: str
    is_template: bool
    organization: Organization
    color: Color
    creator_id: uuid.UUID
    created_at: datetime
    link: str
    items: list[Item] = []

    class Config:
        from_attributes = True


class FormWithoutItems(FormBase):
    id: int
    title: str
    description: str
    is_template: bool
    organization: Organization
    color: Color
    link: str
    created_at: datetime
    creator_id: uuid.UUID

    class Config:
        from_attributes = True
