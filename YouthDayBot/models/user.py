from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel
from schemas.user import SexEnum


class UserModel(BaseModel):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String)
    date_joined: Mapped[datetime] = mapped_column(DateTime)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    additional = relationship("UserAdditionalModel", back_populates="user", foreign_keys="UserAdditionalModel.user_id", uselist=False, lazy="selectin")
    subscribe = relationship("UserSubscribeModel", back_populates="user", foreign_keys="UserSubscribeModel.user_id", lazy="selectin")

class UserAdditionalModel(BaseModel):
    __tablename__ = 'user_additional'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    sex: Mapped[SexEnum | None] = mapped_column(default=None)

    user = relationship("UserModel", back_populates="additional", foreign_keys="UserAdditionalModel.user_id")

class UserSubscribeModel(BaseModel):
    __tablename__ = 'user_subscribe'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    date_joined: Mapped[datetime] = mapped_column(DateTime)

    user = relationship("UserModel", back_populates="subscribe", foreign_keys="UserSubscribeModel.user_id")