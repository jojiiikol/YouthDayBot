from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseModel


class MailingModel(BaseModel):
    __tablename__ = "mailing"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)
