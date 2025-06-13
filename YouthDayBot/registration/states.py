from aiogram.fsm.state import StatesGroup, State


class RegistrationState(StatesGroup):
    name = State()
    sex = State()