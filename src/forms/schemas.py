import uuid
from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from .enums import Color, ItemType, Organization


class OptionBase(BaseModel):
    title: Optional[str] = None


class OptionCreate(OptionBase):
    item_id: int


class OptionUpdate(OptionBase):
    pass


class Option(OptionBase):
    id: int
    title: Optional[str] = None
    item_id: int

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    item_type: ItemType = ItemType.ChoiceQuestion
    required: bool = False


class ItemCreate(ItemBase):
    item_order: int = 1
    form_id: int


class ItemUpdate(ItemBase):
    item_type: Optional[ItemType] = None
    required: Optional[bool] = None


class Item(ItemBase):
    id: int
    title: Optional[str] = None
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
    items: List[Item] = []

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


class OptionUpdateRequest(BaseModel):
    option_id: int
    option: OptionUpdate


# class UpdateSchema(BaseModel):
#     type: Literal['updateForm', 'createItem',
#                   'moveItem', 'deleteItem', 'updateItem', 'createOption',
#                   'deleteOption', 'updateOption']
#     request: Union[FormUpdate, ItemCreate, ItemMove, int,
#                    ItemUpdateRequest, OptionCreate, int, OptionUpdateRequest]
class ItemDelete(BaseModel):
    id: int
    location: int


class UpdateFormRequest(BaseModel):
    updateForm: FormUpdate


class CreateItemRequest(BaseModel):
    createItem: ItemCreate


class MoveItemRequest(BaseModel):
    moveItem: ItemMove


class DeleteItemRequest(BaseModel):
    deleteItem: ItemDelete


class UpdateItemRequest(BaseModel):
    updateItem: ItemUpdateRequest


class CreateOptionRequest(BaseModel):
    createOption: OptionCreate


class DeleteOptionRequest(BaseModel):
    deleteOptionId: int


class UpdateOptionRequest(BaseModel):
    updateOption: OptionUpdateRequest


class UpdateSchema(BaseModel):
    includeFormInResponse: bool
    requests: List[
        Union[
            UpdateFormRequest,
            CreateItemRequest,
            MoveItemRequest,
            DeleteItemRequest,
            UpdateItemRequest,
            CreateOptionRequest,
            DeleteOptionRequest,
            UpdateOptionRequest,
        ]
    ]
