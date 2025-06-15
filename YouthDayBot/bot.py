import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("TOKEN_BOT"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))