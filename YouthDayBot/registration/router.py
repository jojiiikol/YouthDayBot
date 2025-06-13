from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from menu.keyboard import main_menu_keyboard
from registration.keyboard import check_subscribe_keyboard, sex_keyboard
from registration.states import RegistrationState
from repository.user_repository import UserRepository
from schemas.user import UserSchema, CreateUserSchema, AdditionalInfoUserSchema, SexEnum, UserSubscribeSchema

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext, repository: UserRepository = UserRepository()):
    user = await repository.get_user_by_tg_id(message.from_user.id)
    if user:
        user = UserSchema.from_orm(user)
        if user.additional:
            await message.answer("Вы уже прошли этап регистрации")
        else:
            if not user.subscribe:
                await message.answer(
                    f"{user.username}, прошу подписаться на следующие каналы для работы со мной: \n t.me/testBotDMNV2025 \n Канал 2",
                    reply_markup=check_subscribe_keyboard().as_markup()
                )
            else:
                await message.answer("Вы не до конца прошли регистрацию, давайте это исправим!\n\nКак вас зовут?")
                await state.set_state(RegistrationState.name)
    else:
        user = CreateUserSchema(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            date_joined=datetime.now()
        )
        user_model = await repository.create(user)
        user = UserSchema.from_orm(user_model)
        await message.answer(
            f"{user.username}, прошу подписаться на следующие каналы для работы со мной: \n t.me/testBotDMNV2025 \n Канал 2",
            reply_markup=check_subscribe_keyboard().as_markup()
        )

@router.callback_query(F.data == "check_subscribe")
async def check_subscribe(callback: CallbackQuery, bot: Bot, state: FSMContext, repository = UserRepository()):
    member = await bot.get_chat_member("-1002734352735", callback.from_user.id)
    if member.status == 'left':
        await callback.answer(
            "К сожалению вы не подписались на указанные каналы. Подпишитесь и попробуйте еще раз",
            show_alert=True

        )
    else:
        user = await repository.get_user_by_tg_id(callback.from_user.id)
        user = UserSchema.from_orm(user)
        user_data = UserSubscribeSchema(
            user_id = user.id,
            date_joined = datetime.now()
        )
        await repository.create_subscribe(user_data)
        await callback.message.delete()
        await state.set_state(RegistrationState.name)
        await callback.message.answer(
            text="Я увидел твою подписку!\nДавай познакомимся поближе ☺️\n\nКак вас зовут?",
        )

@router.message(RegistrationState.name)
async def set_name(message: Message, state: FSMContext):
    name = message.text.lower().capitalize()

    await state.set_data({"name": name})
    await message.answer(
        text=f"{name} - очень красивое имя!\n\nУкажите ваш пол:",
        reply_markup=sex_keyboard().as_markup()
    )
    await state.set_state(RegistrationState.sex)

@router.callback_query(F.data.startswith("sex_"), RegistrationState.sex)
async def set_user_sex(callback: CallbackQuery, state: FSMContext, repository: UserRepository = UserRepository()):
    await callback.answer()
    await callback.message.delete()

    user = await repository.get_user_by_tg_id(callback.from_user.id)
    user = UserSchema.from_orm(user)
    data = await state.get_data()
    user_data = AdditionalInfoUserSchema(
        user_id=user.id,
        name=data["name"],
        sex=None
    )

    if callback.data == "sex_male":
        user_data.sex = SexEnum.Male
    else:
        user_data.sex = SexEnum.Female

    await repository.create_additional_info(user_data)
    await state.clear()
    await callback.message.answer(text="Спасибо за регистрацию, приятного пользования!☺️",
                                  reply_markup=main_menu_keyboard())






