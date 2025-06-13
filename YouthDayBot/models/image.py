
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel


class ImageModel(BaseModel):
    __tablename__ = 'image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.id'))
    image_path: Mapped[str] = mapped_column(String)

    event = relationship("EventModel", back_populates="images", foreign_keys="ImageModel.event_id")
