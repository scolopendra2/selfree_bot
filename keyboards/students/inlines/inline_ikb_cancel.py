import locale
from datetime import datetime, timedelta, time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import morph


def create_ikb_cancel(items):
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"
    )
    ikb_cancel = InlineKeyboardMarkup(row_width=1)
    for item in items:
        print(item['id'])
        time_from_lesson = item['time_from']
        date_string, time_string = time_from_lesson.split(' ')
        date = datetime.strptime(date_string, "%Y-%m-%d")
        month = date.strftime("%B")
        month_word = morph.parse(month)[0]
        month_name = month_word.inflect({"gent"}).word.capitalize()
        day_of_week = date.strftime("%A").capitalize()
        day = date_string.split('-')[2]
        time_string = ':'.join(time_string.split(':')[:-1])
        text_ikb = f"{day} {month_name} - {day_of_week} {time_string}"
        ikb_cancel.add(InlineKeyboardButton(text=text_ikb, callback_data=f"cancel_{item['id']}"))
    return ikb_cancel


def create_ikb_move(items):
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"
    )
    ikb_move = InlineKeyboardMarkup(row_width=1)
    for item in items:
        time_from_lesson = item['time_from']
        date_string, time_string = time_from_lesson.split(' ')
        date = datetime.strptime(date_string, "%Y-%m-%d")
        month = date.strftime("%B")
        month_word = morph.parse(month)[0]
        month_name = month_word.inflect({"gent"}).word.capitalize()
        day_of_week = date.strftime("%A").capitalize()
        day = date_string.split('-')[2]
        time_string = ':'.join(time_string.split(':')[:-1])
        text_ikb = f"{day} {month_name} - {day_of_week} {time_string}"
        ikb_move.add(InlineKeyboardButton(text=text_ikb, callback_data=f"move_{item['id']}"))
    return ikb_move


def create_ikb_lessons(id_lesson, days):
    help_dict = {
        "1": "6",
        "2": "0",
        "3": "1",
        "4": "2",
        "5": "3",
        "6": "4",
        "7": "5"
    }
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"
    )
    ikb_lessons = InlineKeyboardMarkup(row_width=1)
    now = datetime.now()
    for date in days.split(','):
        day, _time = list(map(lambda x: x.strip(), date.split('T')))
        hour, minute = _time.split(':')
        target_time = time(int(hour), int(minute))
        if now.time() < target_time:
            day = help_dict[day]
            day = now + timedelta(days=(int(day) - now.weekday()) % 7)
            month = day.strftime("%B")
            month_word = morph.parse(month)[0]
            month_name = month_word.inflect({"gent"}).word.capitalize()
            day_of_week = day.strftime("%A").capitalize()
            daay = day.strftime("%d")
            text_ikb = f'{daay} {month_name} {day_of_week} {hour}:{minute}'
            ikb_lessons.add(InlineKeyboardButton(text=text_ikb,
                                                 callback_data=f"ls_{id_lesson}_{date}"))
    return ikb_lessons
