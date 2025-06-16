from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class RegistrationCheckFilter(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery):
        pass