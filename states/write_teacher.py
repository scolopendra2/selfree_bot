from aiogram.dispatcher.filters.state import StatesGroup, State


class WriteTeacher(StatesGroup):
    id_teacher = State()
    send_homework = State()