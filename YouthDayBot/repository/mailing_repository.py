from sqlalchemy import select

from database import new_session
from models.mailing import MailingModel
from schemas.mailing import AddMailingSchema, UpdateMailingSchema


class MailingRepository():
    async def get_all(self):
        async with new_session() as session:
            query = select(MailingModel).order_by(MailingModel.date_time)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_working(self):
        async with new_session() as session:
            query = select(MailingModel).where(MailingModel.finished == False).order_by(MailingModel.date_time)
            result = await session.execute(query)
            return result.scalars().all()

    async def get(self, id: int):
        async with new_session() as session:
            query = select(MailingModel).where(MailingModel.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create(self, mailing_data: AddMailingSchema):
        async with new_session() as session:
            mailing = MailingModel(**mailing_data.dict())
            session.add(mailing)
            await session.flush()
            await session.commit()
            await session.refresh(mailing)
            return mailing

    async def update(self, id: int, mailing_data: UpdateMailingSchema):
        async with new_session() as session:
            query = select(MailingModel).where(MailingModel.id == id)
            mailing = await session.execute(query)
            mailing = mailing.scalar_one()

            for field, value in mailing_data.dict(exclude_unset=True).items():
                setattr(mailing, field, value)

            await session.commit()
            await session.refresh(mailing)
            return mailing
