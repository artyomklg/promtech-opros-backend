from typing import List, Literal, Optional, Union
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

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

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    item_type: ItemType = ItemType.ChoiceQuestion
    item_order: Optional[int] = None
    required: bool = False


class ItemCreate(ItemBase):
    title: str
    item_type: ItemType
    item_order: int
    required: bool
    form_id: int


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    title: str
    item_type: ItemType
    item_order: int
    required: bool
    form_id: int
    options: list[Option] = []

    model_config = ConfigDict(from_attributes=True)


class FormBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_template: bool = False
    organization: Organization = Organization.OKB
    color: Color = Color.Red
    link: Optional[str] = None
    creator_id: Optional[uuid.UUID] = None


class FormCreate(FormBase):
    creator_id: uuid.UUID


class FormUpdate(FormBase):
    is_template: Optional[bool] = None
    organization: Optional[Organization] = None
    color: Optional[Color] = None
    link: Optional[str] = None


class Form(FormBase):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    is_template: bool
    organization: Organization
    color: Color
    creator_id: uuid.UUID
    created_at: datetime
    link: str
    items: Optional[List[Item]] = Field()

    model_config = ConfigDict(from_attributes=True)


class FormWithoutItems(FormBase):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    is_template: bool
    organization: Organization
    color: Color
    link: str
    created_at: datetime
    creator_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ItemMove(BaseModel):
    original_location: int
    new_location: int


class ItemUpdateRequest(BaseModel):
    item_id: int
    item: ItemUpdate


class UpdateSchema(BaseModel):
    type: Literal['updateForm', 'createItem',
                  'moveItem', 'deleteItem', 'updateItem']
    request: Union[FormUpdate, ItemCreate, ItemMove, int, ItemUpdateRequest]
