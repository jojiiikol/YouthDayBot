from aiogram.fsm.state import StatesGroup, State


class AddMailingState(StatesGroup):
    text = State()
    datetime = State()

class EditMailingState(StatesGroup):
    text = State()