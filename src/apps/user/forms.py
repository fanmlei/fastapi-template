from pydantic import BaseModel, EmailStr, Field


class UserLoginForm(BaseModel):
    email: EmailStr
    password: str = Field(...)
