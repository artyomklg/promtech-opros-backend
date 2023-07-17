from typing import Any, Dict, List, Optional, Union
import uuid
from datetime import datetime

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
    title: Optional[str] = None
    description: Optional[str] = None
    is_template: bool = False
    organization: Organization = Organization.OKB
    color: Color = Color.Red
    link: Optional[str] = None
    creator_id: Optional[uuid.UUID] = Field(None)


class FormCreate(FormBase):
    color: Color
    link: str


class FormUpdate(FormBase):
    is_template: Optional[bool] = None
    organization: Optional[Organization] = None
    color: Optional[Color] = None
    link: Optional[str] = None


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


class UpdateSchema(BaseModel):
    includeFormInResponse: bool
    requests: List[Union[Dict[str, Any], str]]
