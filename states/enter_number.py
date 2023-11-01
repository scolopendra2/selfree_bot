from aiogram.dispatcher.filters.state import StatesGroup, State


class EnterNumber(StatesGroup):
    enter_number = State()