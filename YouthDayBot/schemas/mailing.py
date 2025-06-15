from datetime import datetime

from pydantic import BaseModel


class MailingSchema(BaseModel):
    id: int
    text: str
    date_time: datetime
    finished: bool

    class Config:
        from_attributes = True

class AddMailingSchema(BaseModel):
    text: str
    date_time: datetime
    finished: bool = False

class UpdateMailingSchema(BaseModel):
    text: str | None = None
    date_time: datetime | None = None
    finished: bool | None = None
