from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

teacher_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить домашнее задание'), KeyboardButton(text='Прикрепить ссылку на урок')]

    ],
    one_time_keyboard=False,
    resize_keyboard=True
)
