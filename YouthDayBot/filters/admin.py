from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from repository.user_repository import UserRepository


class AdminFilter(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery, repository = UserRepository()):
        user_id = update.from_user.id if (isinstance(update, CallbackQuery)) else update.from_user.id
        user_id = int(user_id)

        user = await repository.get_user_by_tg_id(user_id)
        if not user:
            return False

        if user.is_admin:
            return True
