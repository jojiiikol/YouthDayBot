import datetime
import os

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv

from admin.keyboard import admin_keyboard, admin_event_keyboard, edit_keyboard, cancel_keyboard, manage_event_keyboard, \
    delete_keyboard, edit_images_keyboard, get_statistic_keyboard
from admin.state import AdminState, ChangeEventState, AddEventState
from filters.admin import AdminFilter
from menu.utils import get_event_text_admin, reformat_to_datetime, send_event_admin, send_event, set_data_event, \
    break_long_message
from repository.event_repository import EventRepository
from repository.image_repository import ImageRepository
from repository.user_repository import UserRepository
from schemas.event import EventSchema, UpdateEventSchema, CreateEventSchema
from schemas.image import CreateImageSchema
from schemas.user import UserSchema, UpdateUserSchema

load_dotenv()
router = Router()


@router.message(Command("admin"))
async def admin_registration(message: Message, state: FSMContext, repository=UserRepository()):
    user = await repository.get_user_by_tg_id(message.from_user.id)
    user = UserSchema.from_orm(user)
    if user.is_admin:
        await message.answer(text="Добро пожаловать", reply_markup=admin_keyboard())
    else:
        await message.answer(text="Введите пароль")
        await state.set_state(AdminState.password)


@router.message(AdminState.password)
async def admin_password(message: Message, state: FSMContext, repository=UserRepository()):
    password = message.text
    if password == os.getenv("ADMIN_PASSWORD"):
        user = await repository.get_user_by_tg_id(message.from_user.id)
        user = UpdateUserSchema.from_orm(user)
        user.is_admin = True
        await repository.update(message.from_user.id, user)
        await message.answer(text="Добро пожаловать", reply_markup=admin_keyboard())
    else:
        await message.answer("Доступ запрещен")
    await state.clear()


@router.message(AdminFilter(), F.text == "Управлять мероприятиями")
async def admin_event(message: Message):
    await message.answer(text="Выберите необходимую функцию", reply_markup=manage_event_keyboard())


@router.message(AdminFilter(), F.text == "Изменить мероприятие")
async def change_event(message: Message):
    keyboard = await admin_event_keyboard()
    await message.answer(text="Выберите мероприятие", reply_markup=keyboard)


@router.message(AdminFilter(), F.text == "Обратно в меню")
async def return_to_admin_menu(message: Message):
    await message.answer(text="Выберите функцию", reply_markup=admin_keyboard())


@router.callback_query(F.data.startswith('admin_page_'))
async def admin_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    keyboard = await admin_event_keyboard(page=page)
    await callback.answer()
    await callback.message.edit_text(text="Выберите мероприятие", reply_markup=keyboard)


@router.callback_query(F.data.startswith('admin_event_'))
async def admin_event_change(callback: CallbackQuery, repository=EventRepository()):
    await callback.answer()
    event_id = int(callback.data.split("_")[2])
    event = await repository.get_one(event_id)
    event = EventSchema.from_orm(event)

    await send_event(event, callback, keyboard=edit_keyboard(event_id))


@router.callback_query(F.data.startswith('edit_'))
async def choice_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    operation = callback.data.split("_")[1]
    event_id = callback.data.split("_")[2]

    await state.set_data({
        "operation": operation,
        "event_id": event_id
    })

    if operation == "datetime":
        await callback.message.edit_text(text="Введите новое значение в формате 'ДД-ММ ЧЧ:ММ'",
                                         reply_markup=cancel_keyboard())
        await state.set_state(ChangeEventState.value)
    elif operation == "images":
        await callback.message.edit_text(
            text="Картинки загружаются по одной!",
            reply_markup=edit_images_keyboard(event_id))
    else:
        await callback.message.edit_text(text="Введите новое значение", reply_markup=cancel_keyboard())
        await state.set_state(ChangeEventState.value)


@router.callback_query(F.data.startswith("images_"))
async def edit_image(callback: CallbackQuery, state: FSMContext, image_repository=ImageRepository()):
    operation = callback.data.split("_")[1]
    event_id = int(callback.data.split("_")[2])
    await callback.answer()

    if operation == "delete":
        await callback.message.answer(text="Изображения успешно удалены")
        await image_repository.delete_image(event_id)
    else:
        await callback.message.answer("Загрузите изображения")
        await state.set_state(ChangeEventState.value)


@router.message(ChangeEventState.value)
async def save_change(message: Message, state: FSMContext, bot: Bot, event_repository=EventRepository(),
                      image_repository=ImageRepository()):
    data = await state.get_data()
    event = await event_repository.get_one(int(data['event_id']))
    event = EventSchema.from_orm(event)
    edit_data = UpdateEventSchema()
    if data['operation'] == "datetime":
        date_time = None
        try:
            date_time = reformat_to_datetime(message.text)
        except:
            await message.answer("Неверный формат даты")
        edit_data.date_time = date_time
    elif data['operation'] == "url":
        edit_data.registration_url = message.text
    elif data['operation'] == "images":
        photo = message.photo
        file = await bot.get_file(photo[-1].file_id)
        destination = f"picture/{file.file_id}.jpg"
        await bot.download_file(file.file_path, destination)

        image_data = CreateImageSchema(
            event_id=str(data['event_id']),
            image_path=destination
        )
        try:
            await image_repository.create(image_data)
            await message.answer(text="Изображение загружено")
            await state.clear()
        except:
            await message.answer(text="Произошла ошибка")
        return
    else:
        setattr(edit_data, data['operation'], message.text)

    event = await event_repository.update(event.id, edit_data)
    event = EventSchema.from_orm(event)
    await send_event_admin(event, message)
    await state.clear()


@router.callback_query(F.data == "cancel_edit")
async def cancel_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(text="Выберите необходмую функцию")


@router.message(AdminFilter(), F.text == "Добавить мероприятие")
async def add_event(message: Message, state: FSMContext):
    await state.set_state(AddEventState.name)
    await message.answer(
        text="Напишите название мероприятия", reply_markup=cancel_keyboard())
    event = CreateEventSchema()
    await state.set_data({"event": event})


@router.message(AddEventState.name)
async def add_name(message: Message, state: FSMContext):
    await state.set_state(AddEventState.description)
    await message.answer(
        text="Пропишите описание к мероприятию", reply_markup=cancel_keyboard())
    await set_data_event(state, message.text, "name")


@router.message(AddEventState.description)
async def add_description(message: Message, state: FSMContext):
    await state.set_state(AddEventState.datetime)
    await message.answer(
        text="Укажите время и дату проведения в формате: 'ДД-ММ ЧЧ:ММ'", reply_markup=cancel_keyboard())
    await set_data_event(state, message.text, "description")


@router.message(AddEventState.datetime)
async def add_datetime(message: Message, state: FSMContext):
    try:
        date_time = reformat_to_datetime(message.text)
        await set_data_event(state, date_time, "date_time")
        await message.answer(
            "Укажите ссылку для регистрации", reply_markup=cancel_keyboard())
        await state.set_state(AddEventState.registration_url)
    except:
        await message.answer("Неверный формат даты")
        await message.answer(
            text="Укажите время и дату проведения в формате: 'ДД-ММ ЧЧ:ММ'", reply_markup=cancel_keyboard())
        await state.set_state(AddEventState.datetime)


@router.message(AddEventState.registration_url)
async def add_url(message: Message, state: FSMContext, event_repo=EventRepository()):
    if message.text.capitalize() == 'Отмена':
        await state.clear()
    else:
        await state.set_state(AddEventState.images)
        await set_data_event(state, message.text, "registration_url")
        data = await state.get_data()
        event = data['event']
        event_model = await event_repo.create(event)
        event = EventSchema.from_orm(event_model)
        await state.set_data({'event': event})
        await message.answer(
            text="Мероприятие создано, осталось прикрепить фотографии", reply_markup=cancel_keyboard())


@router.message(AddEventState.images)
async def add_images(message: Message, state: FSMContext, bot: Bot, image_repo=ImageRepository()):
    data = await state.get_data()
    event = data['event']

    photo = message.photo
    if photo:
        file = await bot.get_file(photo[-1].file_id)
        destination = f"picture/{file.file_id}.jpg"
        await bot.download_file(file.file_path, destination)

        image_data = CreateImageSchema(
            event_id=event.id,
            image_path=destination
        )
        await image_repo.create(image_data)

    await message.answer("Изображение загружено")
    await state.clear()


@router.message(AdminFilter(), F.text == "Удалить мероприятие")
async def delete_event(message: Message):
    keyboard = await admin_event_keyboard(callback_data="admin_delete_")
    await message.answer(text="Выберите мероприятие", reply_markup=keyboard)


@router.callback_query(F.data.startswith("admin_delete_"))
async def delete_event(callback: CallbackQuery, repository=EventRepository()):
    await callback.answer()
    event_id = int(callback.data.split("_")[2])
    event = await repository.get_one(event_id)
    await callback.message.edit_text(text=f"Удалить: {event.name}", reply_markup=delete_keyboard(event_id))


@router.callback_query(F.data.startswith("delete_"))
async def delete_event(callback: CallbackQuery, event_repo=EventRepository(), image_repo=ImageRepository()):
    event_id = int(callback.data.split("_")[2])
    operation = callback.data.split("_")[1]

    if operation == "true":
        await image_repo.delete_image(event_id)
        await event_repo.delete(event_id)
        await callback.message.edit_text(text="Мероприятие удалено")
    else:
        await callback.message.edit_text(text="Операция отменена")

@router.message(AdminFilter(), F.text == "Просмотр аналитики")
async def view_analytics(message: Message):
    await message.answer(text="Выберите необходимую функцию", reply_markup=get_statistic_keyboard())


@router.callback_query(F.data == "statistic_views")
async def statistic_views(callback: CallbackQuery, repository = EventRepository()):
    await callback.answer()
    events = await repository.get_all()
    events = [EventSchema.from_orm(event) for event in events]
    message = "<b>Просмотры:</b>\n\n"
    for event in events:
        message += f"{event.name} -- {event.views}\n"
    message = break_long_message(message)
    for text in message:
        await callback.message.answer(text)

@router.callback_query(F.data.startswith("statistic_users"))
async def statistic_users(callback: CallbackQuery, repository=UserRepository()):
    await callback.answer()
    message = "<b>Кол-во зарегистрировавшихся человек в боте: </b>\n"
    registration_data = await repository.get_registration_data()
    for data in registration_data:
        message += f"{data[0]} --> {data[1]}\n"

    subscribers_count = await repository.get_count_subscribers()
    message += f"\n<b>Бот привлек человек на канал: </b> {subscribers_count}"

    message += "\n\n<b>Целевая аудитория: </b>\n"
    sex_count = await repository.get_count_sex_users()
    for user in sex_count:
        if user[0].value == "Male":
            message += f"Мужчин: {user[1]}\n"
        else:
            message += f"Женщин: {user[1]}\n"
    message = break_long_message(message)
    for text in message:
        await callback.message.answer(text=text)

