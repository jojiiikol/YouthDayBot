from sqlalchemy import BigInteger, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from database import new_session
from models.user import UserModel, UserAdditionalModel, UserSubscribeModel
from schemas.user import CreateUserSchema, AdditionalInfoUserSchema, UserSubscribeSchema, UpdateUserSchema


class UserRepository:
    async def create(self, user: CreateUserSchema):
        async with new_session() as session:
            user_model = UserModel(
                tg_id=user.tg_id,
                username=user.username,
                date_joined=user.date_joined,
            )
            session.add(user_model)
            await session.flush()
            await session.commit()
            await session.refresh(user_model)
            return user_model

    async def create_additional_info(self, user_data: AdditionalInfoUserSchema):
        async with new_session() as session:
            user_data = UserAdditionalModel(**user_data.dict())
            session.add(user_data)
            await session.flush()
            await session.commit()
            await session.refresh(user_data)
            return user_data

    async def create_subscribe(self, user_data: UserSubscribeSchema):
        async with new_session() as session:
            user_data = UserSubscribeModel(**user_data.dict())
            session.add(user_data)
            await session.flush()
            await session.commit()
            await session.refresh(user_data)
            return user_data

    async def get_user_by_tg_id(self, tg_id: BigInteger) -> UserModel:
        async with new_session() as session:
            query = select(UserModel).options(selectinload(UserModel.additional), selectinload(UserModel.subscribe)).filter(UserModel.tg_id == tg_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            return result

    async def update(self, tg_id: int, user_data: UpdateUserSchema):
        async with new_session() as session:
            query = select(UserModel).filter(UserModel.tg_id == tg_id)
            result = await session.execute(query)
            user = result.scalar_one()

            for field, value in user_data.dict(exclude_unset=True).items():
                setattr(user, field, value)

            await session.commit()
            await session.refresh(user)
            return user

    async def get_all_username(self):
        async with new_session() as session:
            query = select(UserModel.tg_id)
            result = await session.execute(query)
            return result.scalars().all()

