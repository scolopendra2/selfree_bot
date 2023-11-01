from aiogram.dispatcher.filters.state import StatesGroup, State


class Pay(StatesGroup):
    data_pay = State()