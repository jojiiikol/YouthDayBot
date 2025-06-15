from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from admin.keyboard import admin_keyboard
from mailing.keyboard import mailing_menu_keyboard, cancel_keyboard, mailing_keyboard
from mailing.scheduler import scheduler
from mailing.state import AddMailingState
from mailing.utils import mailing_to_users
from menu.utils import reformat_to_datetime, break_long_message
from repository.mailing_repository import MailingRepository
from schemas.mailing import AddMailingSchema, MailingSchema

router = Router()


@router.message(F.text == "Управлять рассылкой")
async def mailing_menu(message: Message):
    await message.answer(text="Выберите необходимую функцию", reply_markup=mailing_menu_keyboard())


@router.message(F.text == "В меню")
async def mailing_menu(message: Message):
    await message.answer(text="Выберите необходимую функцию", reply_markup=admin_keyboard())


@router.message(F.text == "Запланировать сообщение")
async def add_mailing(message: Message, state: FSMContext):
    await message.answer("Напишите текст для рассылки", reply_markup=cancel_keyboard())
    await state.set_state(AddMailingState.text)


@router.message(AddMailingState.text)
async def add_mailing_text(message: Message, state: FSMContext):
    await state.set_data({"text": message.text})
    await message.answer(text="Укажите время и дату отправки сообщения: 'ДД-ММ ЧЧ:ММ'", reply_markup=cancel_keyboard())
    await state.set_state(AddMailingState.datetime)


@router.message(AddMailingState.datetime)
async def add_mailing_datetime(message: Message, state: FSMContext, bot: Bot, repository=MailingRepository(),
                               schedule=scheduler):
    date_time = reformat_to_datetime(message.text)
    data = await state.get_data()
    mailing_data = AddMailingSchema(
        text=data['text'],
        date_time=date_time
    )
    mailing = await repository.create(mailing_data)
    mailing = MailingSchema.from_orm(mailing)
    schedule.add_job(mailing_to_users, 'date', next_run_time=date_time, args=[mailing])
    await message.answer(text="Рассылка успешно создана!")
    await state.clear()


# except:
#     await message.answer(text="Неверный формат, укажите время и дату отправки сообщения: 'ДД-ММ ЧЧ:ММ'")
#     await state.set_state(AddMailingState.datetime)


@router.callback_query(F.data == "mailing_cancel_add")
async def cancel_add_mailing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer(text="Операция отменена")


@router.message(F.text == "Рассылки в работе")
async def show_mailing(message: Message):
    keyboard = await mailing_keyboard()
    await message.answer(text="Выберите рассылку", reply_markup=keyboard)


@router.callback_query(F.data.startswith("mailing_page_"))
async def update_keyboard(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    keyboard = await mailing_keyboard(page)
    await callback.message.edit_text(text="Выберите рассылку", reply_markup=keyboard)


@router.callback_query(F.data.startswith("get_mailing_"))
async def get_mailing(callback: CallbackQuery, repository=MailingRepository()):
    mailing_id = int(callback.data.split("_")[2])
    mailing = await repository.get(mailing_id)
    mailing = MailingSchema.from_orm(mailing)

    date = mailing.date_time.date().strftime('%d.%m')
    time = mailing.date_time.time().strftime('%H:%M')

    message_text = f"<b>ДАТА И ВРЕМЯ: </b>{date} {time}\n\n{mailing.text}"
    reformat_text = break_long_message(message_text)

    await callback.answer()
    for text in reformat_text:
        await callback.message.answer(text)
