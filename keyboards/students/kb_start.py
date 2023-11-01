from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Осталось уроков'), KeyboardButton(text='Отменить'), KeyboardButton(text='Перенести')],
        [KeyboardButton(text='Расписание')],
        [KeyboardButton(text='Тех. Поддержка'), KeyboardButton(text='Выход')]

    ],
    one_time_keyboard=True,
    resize_keyboard=True
)