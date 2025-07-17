from typing import ClassVar

from passlib.context import CryptContext
from tortoise import fields, models

from src.core.model import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(models.Model):
    userid = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=32, unique=True, description="用户名")
    hashed_password = fields.CharField(max_length=128, description="密码")
    email = fields.CharField(max_length=100, unique=True, description="邮箱")
    is_active = fields.BooleanField(default=True, description="是否激活")
    is_superuser = fields.BooleanField(default=False, description="是否超级用户")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "auth_user"

    class PydanticMeta:
        exclude: ClassVar[list] = ["hashed_password"]

    def set_password(self, plain_password: str) -> None:
        self.hashed_password = pwd_context.hash(plain_password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def __str__(self) -> str:
        return self.username
