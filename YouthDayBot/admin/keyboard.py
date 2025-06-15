from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from repository.event_repository import EventRepository
from schemas.event import EventSchema


def admin_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="Управлять мероприятиями"),
        KeyboardButton(text="Управлять рассылкой"),
        KeyboardButton(text="Просмотр аналитики"),
        KeyboardButton(text="◀️ Назад")
    )
    return keyboard.adjust(2, 1, 1).as_markup(resize_keyboard = True)


async def admin_event_keyboard(page=0, repository=EventRepository(), callback_data="admin_event_"):
    events = await repository.get_all()
    events = [EventSchema.from_orm(event) for event in events]

    limit = 5
    start = page * limit
    end = start + limit

    keyboard = InlineKeyboardBuilder()
    break_events = events[start:end]

    for event in break_events:
        keyboard.add(
            InlineKeyboardButton(text=f"{event.name}", callback_data=f"{callback_data}{event.id}"),
        )
    keyboard.adjust(1)

    if page == 0:
        if len(events) <= end:
            pass
        else:
            keyboard.row(
                InlineKeyboardButton(text="Вперед", callback_data=f"admin_page_{page + 1}"),
            )
    else:
        if len(events) <= end:
            keyboard.row(
                InlineKeyboardButton(text="Назад", callback_data=f"admin_page_{page - 1}"),
            )
        else:
            keyboard.row(
                InlineKeyboardButton(text="Назад", callback_data=f"admin_page_{page - 1}"),
                InlineKeyboardButton(text="Вперед", callback_data=f"admin_page_{page + 1}"),
            )
    return keyboard.as_markup()

def edit_keyboard(event_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Изменить название", callback_data=f"edit_name_{event_id}"),
        InlineKeyboardButton(text="Изменить дату и время", callback_data=f"edit_datetime_{event_id}"),
        InlineKeyboardButton(text="Изменить описание", callback_data=f"edit_description_{event_id}"),
        InlineKeyboardButton(text="Изменить ссылку", callback_data=f"edit_url_{event_id}"),
        InlineKeyboardButton(text="Изменить изображения", callback_data=f"edit_images_{event_id}"),
        InlineKeyboardButton(text="Назад", callback_data="admin_page_0")
    )
    return keyboard.adjust(2, 2, 1, 1).as_markup()

def cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Отменить", callback_data="cancel_edit")
    )
    return keyboard.as_markup()

def manage_event_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="Добавить мероприятие"),
        KeyboardButton(text="Изменить мероприятие"),
        KeyboardButton(text="Удалить мероприятие"),
        KeyboardButton(text="Обратно в меню")
    )
    return keyboard.adjust(2, 1, 1).as_markup(resize_keyboard=True)

def delete_keyboard(event_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Подтвердить", callback_data=f"delete_true_{event_id}"),
        InlineKeyboardButton(text="Отменить", callback_data=f"delete_false_{event_id}")
    )
    return keyboard.adjust(2).as_markup()

def edit_images_keyboard(event_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Удалить", callback_data=f"images_delete_{event_id}"),
        InlineKeyboardButton(text="Загрузить", callback_data=f"images_load_{event_id}"),
        InlineKeyboardButton(text="Отменить", callback_data="cancel_edit")
    )
    return keyboard.adjust(2, 1).as_markup()