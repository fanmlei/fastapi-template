from contextvars import ContextVar
from datetime import datetime
from tortoise import fields, models
from tortoise.queryset import QuerySet
from typing import TypeVar, Type, Any, Optional

current_user_id: ContextVar[int | None] = ContextVar('current_user_id', default=None)
_BaseModel = TypeVar('_BaseModel', bound='BaseModel')

class BaseModel(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    user_id = fields.IntField(index=True, description="用户ID")

    class Meta:
        abstract = True

    @classmethod
    def query(cls: Type[_BaseModel]) -> QuerySet[_BaseModel]:
        return super().query().filter(user_id=get_current_user_id())