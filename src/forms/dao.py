from .models import OptionModel, ItemModel, FormModel
from .schemas import (
    OptionCreate, OptionUpdate,
    ItemCreate, ItemUpdate,
    FormCreate, FormUpdate
)
from ..dao import BaseDAO


class OptionDAO(BaseDAO[OptionModel, OptionCreate, OptionUpdate]):
    model = OptionModel


class ItemDAO(BaseDAO[ItemModel, ItemCreate, ItemUpdate]):
    model = ItemModel


class FormDAO(BaseDAO[FormModel, FormCreate, FormUpdate]):
    model = FormModel
