from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: int
    image_path: str

    class Config:
        from_attributes = True

class CreateImageSchema(BaseModel):
    event_id: int
    image_path: str