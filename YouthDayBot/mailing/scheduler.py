import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()


jobstores = {
    "default": SQLAlchemyJobStore(url=os.getenv('DATABASE_SCHEDULE_URL'))
}


scheduler = AsyncIOScheduler(jobstores=jobstores)

