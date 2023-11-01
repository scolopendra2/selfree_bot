from aiogram.dispatcher.filters.state import StatesGroup, State


class SendLink(StatesGroup):
    enter_id = State()
    enter_link = State()