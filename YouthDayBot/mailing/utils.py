import asyncio

from aiogram import Bot

from bot import bot
from mailing.scheduler import scheduler
from repository.mailing_repository import MailingRepository
from repository.user_repository import UserRepository
from schemas.mailing import MailingSchema, UpdateMailingSchema


async def mailing_to_users(mailing_data: MailingSchema, repository=UserRepository()):
    actual_mailing = await get_mailing(mailing_data.id)
    usernames = await repository.get_all_username()
    for username in usernames:
        await bot.send_message(username, actual_mailing.text)
        await asyncio.sleep(1)
    await finish_mailing(mailing_data.id)

async def get_mailing(id: int, repository=MailingRepository()):
    mailing = await repository.get(id)
    mailing = MailingSchema.from_orm(mailing)
    return mailing
async def finish_mailing(id: int, mailing_repository=MailingRepository()):
    finished_schema = UpdateMailingSchema(
        finished=True
    )
    await mailing_repository.update(id, finished_schema)
