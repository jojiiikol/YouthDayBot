from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def check_subscribe_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Проверить подписки",
            callback_data="check_subscribe"
        )
    )
    return keyboard

def sex_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="👨 Мужской",
            callback_data="sex_male"
        ),
        InlineKeyboardButton(
            text="👩 Женский",
            callback_data="sex_female"
        )
    )
    return keyboard