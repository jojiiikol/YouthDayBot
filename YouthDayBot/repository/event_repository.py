from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from database import new_session
from models.event import EventModel
from models.image import ImageModel
from schemas.event import EventSchema, UpdateEventSchema, CreateEventSchema


class EventRepository():
    async def get_all(self):
        async with new_session() as session:
            query = select(EventModel).options(selectinload(EventModel.images)).order_by(EventModel.date_time)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_one(self, id: int):
        async with new_session() as session:
            query = select(EventModel).options(selectinload(EventModel.images)).where(EventModel.id == id)
            result = await session.execute(query)
            return result.scalar_one()

    async def create(self, event_data: CreateEventSchema):
        async with new_session() as session:
            event = EventModel(**event_data.dict())
            session.add(event)
            await session.flush()
            await session.commit()
            await session.refresh(event)
            return event

    async def delete(self, event_id: int):
        async with new_session() as session:
            query = delete(EventModel).where(EventModel.id == event_id)
            await session.execute(query)
            await session.commit()

    async def update(self, event_id: int, event_data: UpdateEventSchema):
        async with new_session() as session:
            query = select(EventModel).options(selectinload(EventModel.images)).where(EventModel.id == event_id)
            result = await session.execute(query)

            event_model = result.scalar_one()
            for field, value in event_data.dict(exclude_unset=True).items():
                setattr(event_model, field, value)

            await session.commit()
            await session.refresh(event_model)

            return event_model