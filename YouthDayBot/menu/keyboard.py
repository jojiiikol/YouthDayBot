from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from repository.event_repository import EventRepository
from schemas.event import EventSchema


def main_menu_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="🤹 О неделе молодёжи «Север Молодой»"),
        KeyboardButton(text="📆 Программа недели"),
        KeyboardButton(text="🥳 Карта Дня Молодежи - 2025"),
        KeyboardButton(text="🎟️ О розыгрыше"),
        KeyboardButton(text="✉️ Связь с организатором")
                 )
    return keyboard.adjust(1, 2, 1, 1).as_markup(resize_keyboard=True, input_field_placeholder="Клик :)")

def get_blocks_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="🔵 Движение", callback_data="block_move"),
        InlineKeyboardButton(text="🟡 Единство", callback_data="block_unity"),
        InlineKeyboardButton(text="🟠 Память", callback_data="block_memory"),
        InlineKeyboardButton(text="🟣 Любовь", callback_data="block_love"),
        InlineKeyboardButton(text="🟢 Свобода", callback_data="block_freedom"),
        InlineKeyboardButton(text="🎤 Cцена", callback_data="block_scene"),
    )
    return keyboard.adjust(2, 2, 2).as_markup()

def week_info_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="🗓️ Полное расписание"),
        KeyboardButton(text="📜 Узнать подробно"),
        KeyboardButton(text="◀️ Назад")
    )
    return keyboard.adjust(2, 1).as_markup(resize_keyboard=True)

async def events_keyboard(page = 0, repository = EventRepository()):
    events = await repository.get_all()
    events = [EventSchema.from_orm(event) for event in events]

    limit = 5
    start = page * limit
    end = start + limit

    events_break = events[start:end]

    keyboard = InlineKeyboardBuilder()
    for event in events_break:
        keyboard.add(
            (InlineKeyboardButton(text=event.name, callback_data=f"event_{event.id}"))
        )
    keyboard.adjust(1)

    if page == 0:
        if (len(events) <= end):
            pass
        else:
            keyboard.row(
                InlineKeyboardButton(text="➡️", callback_data=f"event_page_{page + 1}")
            )
    else:
        if (len(events) <= end):
            keyboard.row(
                InlineKeyboardButton(text="⬅️", callback_data=f"event_page_{page - 1}")
            )
        else:
            keyboard.row(
                InlineKeyboardButton(text="⬅️", callback_data=f"event_page_{page - 1}"),
                InlineKeyboardButton(text="➡️", callback_data=f"event_page_{page + 1}"),

            )

    return keyboard


