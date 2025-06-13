from datetime import datetime
from typing import List

from pydantic import BaseModel

from schemas.image import ImageSchema


class EventSchema(BaseModel):
    id: int
    name: str
    date_time: datetime | None
    image_path: str | None
    description: str | None
    views: int
    registration_url: str | None
    images: List[ImageSchema] | None

    class Config:
        from_attributes = True

class CreateEventSchema(BaseModel):
    name: str | None = None
    date_time: datetime | None = None
    image_path: str | None = None
    description: str | None = None
    registration_url: str | None = None

class UpdateEventSchema(BaseModel):
    name: str | None = None
    date_time: datetime | None = None
    image_path: str | None = None
    description: str | None = None
    views: int | None = None
    registration_url: str | None = None