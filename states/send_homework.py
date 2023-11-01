from aiogram.dispatcher.filters.state import StatesGroup, State


class SendHomework(StatesGroup):
    enter_id = State()
    enter_homework = State()