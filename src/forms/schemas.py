import enum
import uuid

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
    ...


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
    ...


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
    organiztion: Organization | None = Organization.OKB
    color: Color | None = Color.Orange
    creator_id: uuid.UUID | None = Field(default='a8abc8e7-c90c-48a4-bb58-bfd5e291ed66')


class FormCreate(FormBase):
    title: str
    organiztion: Organization
    color: Color


class FormUpdate(FormBase):
    ...


class Form(FormBase):
    id: int
    title: str
    description: str
    is_template: bool
    organiztion: Organization
    color: Color
    creator_id: uuid.UUID
    items: list[Item] = []

    class Config:
        orm_mode = True


class FormWithoutItems(BaseModel):
    id: int
    title: str
    description: str
    is_template: bool
    organiztion: Organization
    color: Color
    creator_id: uuid.UUID

    class Config:
        orm_mode = True
