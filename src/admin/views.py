from sqladmin import ModelView

from src.forms.models import FormModel, ItemModel, OptionModel
from src.forms.reviews.models import AnswerModel, ReviewModel
from src.users.models import RefreshSessionModel, UserModel


class UserAdmin(ModelView, model=UserModel):
    column_list = []
    column_details_exclude_list = []
    can_delete = False
    name = ""
    name_plural = ""


class RefreshSessionAdmin(ModelView, model=RefreshSessionModel):
    column_list = []
    column_details_exclude_list = []
    name = ""
    name_plural = ""


class OptionAdmin(ModelView, model=OptionModel):
    column_list = []
    column_details_exclude_list = []
    name = ""
    name_plural = ""


class ItemAdmin(ModelView, model=ItemModel):
    column_list = []
    column_details_exclude_list = []
    name = ""
    name_plural = ""


class FormAdmin(ModelView, model=FormModel):
    column_list = []
    column_details_exclude_list = []
    name = ""
    name_plural = ""


class AnswerAdmin(ModelView, model=AnswerModel):
    column_list = []
    column_details_exclude_list = []
    name = ""
    name_plural = ""


class ReviewAdmin(ModelView, model=ReviewModel):
    column_list = []
    column_details_exclude_list = []
    name = ""
    name_plural = ""
