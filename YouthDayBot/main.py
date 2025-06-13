import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from registration.router import router as reg_router
from menu.router import router as menu_router
from admin.router import router as admin_router

load_dotenv()

bot = Bot(token=os.getenv("TOKEN_BOT"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(reg_router)
dp.include_router(menu_router)
dp.include_router(admin_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot Started")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())