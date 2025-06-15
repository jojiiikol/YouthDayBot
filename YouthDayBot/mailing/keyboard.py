from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from repository.mailing_repository import MailingRepository
from schemas.mailing import MailingSchema


def mailing_menu_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="Запланировать сообщение"),
        KeyboardButton(text="Рассылки в работе"),
        KeyboardButton(text="В меню")
    )
    return keyboard.adjust(2, 1).as_markup(resize_keyboard=True)

def cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Отменить", callback_data="mailing_cancel_add"),
    )
    return keyboard.as_markup()

async def mailing_keyboard(page=0, repository=MailingRepository()):
    mailings = await repository.get_working()
    mailings_schema = [MailingSchema.from_orm(mailing) for mailing in mailings]

    limit = 5
    start = page * limit
    end = start + limit

    part_mailing = mailings_schema[start:end]

    keyboard = InlineKeyboardBuilder()
    for mailing in part_mailing:
        keyboard.add(
            InlineKeyboardButton(text=str(mailing.date_time), callback_data=f"get_mailing_{mailing.id}")
        )

    keyboard.adjust(1)

    if page == 0:
        if len(mailings_schema) <= end:
            pass
        else:
            keyboard.row(
                InlineKeyboardButton(text="Вперед", callback_data=f"mailing_page_{page + 1}"),
            )
    else:
        if len(mailings_schema) <= end:
            keyboard.row(
                InlineKeyboardButton(text="Назад", callback_data=f"mailing_page_{page - 1}"),
            )
        else:
            keyboard.row(
                InlineKeyboardButton(text="Назад", callback_data=f"mailing_page_{page - 1}"),
                InlineKeyboardButton(text="Вперед", callback_data=f"mailing_page_{page + 1}"),
            )
    return keyboard.as_markup()


