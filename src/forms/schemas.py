import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemType(str, enum.Enum):
    ChoiceQuestion = 'choiceQuestion'
    ScaleQuestion = 'multychoiceQuestion'
    TextQuestion = 'textQuestion'
    LongTextQuestion = 'longTextQuestion'


class Color(str, enum.Enum):
    Red = 'red'
    Orange = '#F48221'
    Yellow = 'Yellow'
    LimeGreen = 'LimeGreen'
    Aqua = 'Aqua'
    MediumBlue = 'MediumBlue'
    DarkOrchid = 'DarkOrchid'
    Black = 'Black'


class Organization(str, enum.Enum):
    OKB = 'okb.jpg'
    PROMTEX = 'promtex.jpg'
    PROMTEXIRK = 'promtexirk.jpg'
    PROMTEXKAZ = 'promtexkaz.jpg'
    ZAVOD = 'zavod.jpg'
    ATOMSPEC = 'atomspec.jpg'
    KAZZAVOD = 'kazzavod.jpg'
    LOGO1 = 'logo1.jpg'


class OptionBase(BaseModel):
    title: str | None = None
    item_id: int | None = None


class OptionCreate(OptionBase):
    title: str
    item_id: int


class OptionUpdate(OptionBase):
    id: int | None
    title: str
    item_id: int | None

    class Config():
        orm_mode = True


class Option(OptionBase):
    id: int
    title: str
    item_id: int

    class Config():
        orm_mode = True


class ItemBase(BaseModel):
    title: str | None = None
    description: str | None = None
    item_type: ItemType | None = None
    item_order: int | None = None
    required: bool = False
    form_id: int | None = None


class ItemCreate(ItemBase):
    title: str
    description: str | None = None
    item_type: ItemType
    item_order: int
    required: bool
    form_id: int


class ItemUpdate(ItemBase):
    id: int | None
    title: str
    item_type: ItemType
    item_order: int
    required: bool
    form_id: int | None
    options: list[OptionUpdate] = []

    class Config():
        orm_mode = True


class Item(ItemBase):
    id: int
    title: str
    item_type: ItemType
    item_order: int
    required: bool
    form_id: int
    options: list[Option] = []

    class Config():
        orm_mode = True


class FormBase(BaseModel):
    title: str | None = None
    description: str | None = None
    is_template: bool = False
    organization: Organization | None = Organization.OKB
    color: Color | None = Color.Orange
    created_at: datetime | None
    link: str | None
    creator_id: uuid.UUID | None = Field(default='a8abc8e7-c90c-48a4-bb58-bfd5e291ed66')


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
        orm_mode = True


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
        orm_mode = True


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
        orm_mode = True
