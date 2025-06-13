from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    password = State()

class ChangeEventState(StatesGroup):
    value = State()

class AddEventState(StatesGroup):
    name = State()
    description = State()
    datetime = State()
    registration_url = State()
    images = State()