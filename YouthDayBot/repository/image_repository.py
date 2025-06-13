from sqlalchemy import delete

from database import new_session
from models.image import ImageModel
from schemas.image import CreateImageSchema


class ImageRepository:
    async def create(self, image_data: CreateImageSchema):
        async with new_session() as session:
            image = ImageModel(**image_data.dict())
            session.add(image)
            await session.flush()
            await session.commit()
            return image

    async def delete_image(self, event_id: int):
        async with new_session() as session:
            query = delete(ImageModel).where(ImageModel.event_id == event_id)
            result = await session.execute(query)
            await session.commit()