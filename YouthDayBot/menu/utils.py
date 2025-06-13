import datetime
from typing import List, Any

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram.utils.media_group import MediaGroupBuilder

from admin.keyboard import edit_keyboard
from schemas.event import EventSchema



async def send_event_admin(event: EventSchema, message: Message):
    text = get_event_text_admin(event)
    if len(text) > 1:
        await send_photo_admin(event, message)
        for msg in text[0: len(text) - 1]:
            await message.answer(text=msg)
        await message.answer(text=text[len(text) - 1], reply_markup=edit_keyboard(event.id))
    else:
        if len(text[0]) > 1024:
            await send_photo_admin(event, message)
            await message.answer(text[0], reply_markup=edit_keyboard(event.id))
        else:
            if event.images:
                media = MediaGroupBuilder(caption=text[0])
                for photo in event.images:
                    photo = FSInputFile(path=photo.image_path)
                    media.add_photo(photo)
                await message.answer_media_group(media.build())
                await message.answer("Выберите функцию", reply_markup=edit_keyboard(event.id))
            else:
                await message.answer(text[0], reply_markup=edit_keyboard(event.id))
async def send_event(event: EventSchema, callback: CallbackQuery, keyboard = None):
    text = get_event_text(event)
    if len(text) > 1:
        await send_photo(event, callback)
        if keyboard is None:
            for message in text[0: len(text)]:
                await callback.message.answer(text=message)
        else:
            for msg in text[0: len(text) - 1]:
                await callback.message.answer(text=msg)
            await callback.message.answer(text=text[len(text) - 1], reply_markup=keyboard)
    else:
        if len(text[0]) > 1024:
            await send_photo(event, callback)
            await callback.message.answer(text[0], reply_markup=keyboard)
        else:
            if event.images:
                media = MediaGroupBuilder(caption=text[0])
                for photo in event.images:
                    photo = FSInputFile(path=photo.image_path)
                    media.add_photo(photo)
                await callback.message.answer_media_group(media.build())
                if keyboard:
                    await callback.message.answer("Выберите функцию", reply_markup=keyboard)

            else:
                await callback.message.answer(text[0], reply_markup=keyboard)


async def send_photo_admin(event: EventSchema, message: Message):
    if event.images:
        for photo in event.images:
            photo = FSInputFile(path=photo.image_path)
            await message.answer_photo(photo=photo)
async def send_photo(event: EventSchema, callback: CallbackQuery):
    if event.images:
        for photo in event.images:
            photo = FSInputFile(path=photo.image_path)
            await callback.message.answer_photo(photo=photo)


def break_long_message(text: str) -> List[str]:
    text_list = []
    if len(text) > 4096:
        for i in range(0, len(text), 4096):
            part_text = text[i:i + 4096]
            opened_tag = part_text.rfind("<b>")
            closed_tag = part_text.rfind("</b>")

            if opened_tag == -1 and closed_tag == -1:
                pass
            elif opened_tag == -1:
                part_text = part_text[0:closed_tag] + part_text[closed_tag + 4:]
            elif opened_tag > closed_tag:
                part_text = part_text[0:opened_tag] + part_text[opened_tag + 3:]

            text_list.append(part_text)
    else:
        text_list.append(text)
    return text_list


def get_event_text(event: EventSchema) -> List[str]:
    date = event.date_time.date().strftime('%d.%m')
    time = event.date_time.time().strftime('%H:%M')

    text = f"<b>{event.name}</b>\n\n<b>Дата: {date}</b>\n<b>Время: {time}</b>\n\n{event.description}\n\n<b>Ссылка для регистрации:</b> {event.registration_url}"
    return break_long_message(text)


def get_event_text_admin(event: EventSchema) -> List[str]:
    date = event.date_time.date().strftime('%d.%m')
    time = event.date_time.time().strftime('%H:%M')

    text = f"<b>НАЗВАНИЕ: {event.name}</b>\n\n<b>ДАТА: {date}</b>\n<b>ВРЕМЯ: {time}</b>\n\n<b>ОПИСАНИЕ: </b>{event.description}\n\n<b>ССЫЛКА: </b> {event.registration_url}"
    return break_long_message(text)


def reformat_to_datetime(date: str):
    date_time = date.split(" ")
    date = date_time[0].split("-")
    time = date_time[1].split(":")
    date_time = datetime.datetime(year=2025, month=int(date[1]), day=int(date[0]), hour=int(time[0]),
                                  minute=int(time[1]))
    return date_time

async def set_data_event(state: FSMContext, data: Any, name: str):
    state_data = await state.get_data()
    event = state_data["event"]
    setattr(event, name, data)
    await state.set_data({"event": event})
