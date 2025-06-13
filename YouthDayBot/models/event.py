from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel
from models.image import ImageModel


class EventModel(BaseModel):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    views: Mapped[int] = mapped_column(Integer, default=0)
    registration_url: Mapped[str] = mapped_column(String, nullable=True)

    images = relationship(ImageModel, back_populates="event", foreign_keys="ImageModel.event_id", lazy="selectin")
