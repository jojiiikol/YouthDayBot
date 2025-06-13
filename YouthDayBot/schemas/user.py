from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel
from sqlalchemy import BigInteger

class SexEnum(Enum):
    Male = "Male"
    Female = "Female"

class UserSubscribeSchema(BaseModel):
    user_id: int
    date_joined: datetime

    class Config:
        from_attributes = True

class AdditionalInfoUserSchema(BaseModel):
    user_id: int
    name: str | None
    sex: SexEnum | None

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    id: int
    tg_id: int
    username: str
    date_joined: datetime
    is_admin: bool
    additional: AdditionalInfoUserSchema | None
    subscribe: list[UserSubscribeSchema] | None

    class Config:
        from_attributes = True

class CreateUserSchema(BaseModel):
    tg_id: int
    username: str
    date_joined: datetime


class UpdateUserSchema(BaseModel):
    tg_id: int | None = None
    username: str | None = None
    date_joined: datetime | None = None
    is_admin: bool = False

    class Config:
        from_attributes = True





