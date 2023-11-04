import datetime
import json
import os
from datetime import timedelta

import requests
from aiogram import types

from keyboards.students.inlines import create_ikb_move, create_ikb_lessons
from loader import dp, db
from models import User
from keyboards.students import start_kb


def get_items(user):  # функция для получения уроков пользователя
    url_lesson = "https://selfree.s20.online/v2api/1/lesson/index"
    now = datetime.datetime.now()
    end_date = now + datetime.timedelta(days=30)
    data_check = {
        "customer_id": user.crm_user_id,
        "status": 1,
        "date_from": str(now).split()[0],
        "date_to": str(end_date).split()[0]
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    response = requests.post(url_lesson, data=json.dumps(data_check), headers=headers)
    return response.json()['items']


async def get_teacher_freelesson(user):
    url_study = "https://selfree.s20.online/v2api/1/customer/index"
    url_teacher = "https://selfree.s20.online/v2api/1/teacher/index"
    data_check = {
        "phone": user.phone
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    response_study = requests.post(url_study, data=json.dumps(data_check), headers=headers)
    try:
        teacher_name = response_study.json()['items'][0]['teacher_ids'][0]
    except Exception:
        return "Нет учителя"
    data_check = {
        "name": teacher_name
    }
    teacher_lessons = requests.post(url_teacher, data=json.dumps(data_check), headers=headers)
    return teacher_lessons.json()['items'][0]['custom_listfreelessons']


def get_left_lesson(user):  # функция для получения оставшихся оплаченных уроков(чтобы в InlineKeyboard были только они)
    url_study = "https://selfree.s20.online/v2api/1/customer/index"
    data_check = {
        "phone": user.phone
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    response_study = requests.post(url_study, data=json.dumps(data_check), headers=headers)
    return response_study.json()['items'][0]['paid_lesson_count']


@dp.message_handler(text='Перенести')
async def move(message: types.Message):
    user = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    if user is None:
        await message.answer("Вы не вошли в аккаунт", reply_markup=start_kb)
    else:
        remains = get_left_lesson(user)
        items = get_items(user)[::-1][:remains]
        await message.answer("Выберите урок, который хотите перенести", reply_markup=create_ikb_move(items))


@dp.callback_query_handler(lambda query: query.data.startswith('move_'))
async def move_id(call: types.CallbackQuery):
    user = db.query(User).filter(User.tg_user_id == call.from_user.id).first()
    days = await get_teacher_freelesson(user)
    id_lesson = call.data.split('_')[1]
    ikb = create_ikb_lessons(id_lesson, days)
    await call.message.answer('Выберите день на который хотите перенести урок', reply_markup=ikb)


def get_difference(id_lesson):
    url_lesson = f"https://selfree.s20.online/v2api/1/lesson/update?id={id_lesson}"
    data_check = {
        "note": ""
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }

    response_lesson = requests.post(url_lesson, data=json.dumps(data_check), headers=headers)
    date_string1 = response_lesson.json()['model']['time_from']
    date_string2 = response_lesson.json()['model']['time_to']
    date1 = datetime.datetime.strptime(date_string1, "%Y-%m-%d %H:%M:%S")
    date2 = datetime.datetime.strptime(date_string2, "%Y-%m-%d %H:%M:%S")
    difference = date2 - date1
    hours_difference = difference.total_seconds() / 3600
    return hours_difference


@dp.callback_query_handler(lambda query: query.data.startswith('ls_'))
async def move_id(call: types.CallbackQuery):
    _, id_lesson, date = call.data.split('_')
    day, time_1 = list(map(lambda x: x.strip(), date.split('T')))
    help_dict = {
        "1": "6",
        "2": "0",
        "3": "1",
        "4": "2",
        "5": "3",
        "6": "4",
        "7": "5"
    }
    now = datetime.datetime.now()
    day = help_dict[day]
    day = now + timedelta(days=(int(day) - now.weekday()) % 7)
    y_m_d = day.strftime('%y-%m-%d')
    difference = get_difference(id_lesson)
    time_from = f"{y_m_d} {time_1}:01"
    time_obj = datetime.datetime.strptime(time_1, '%H:%M').time()
    seconds_to_add = int(difference * 3600 + 60)
    time_delta = datetime.timedelta(seconds=seconds_to_add)
    new_time_obj = (datetime.datetime.combine(datetime.date.today(), time_obj) + time_delta).time()
    new_time_str = new_time_obj.strftime('%H:%M')
    time_to = f"{y_m_d} {new_time_str}:00"
    url_lesson = "https://selfree.s20.online/v2api/1/lesson/update?id=49886"
    data_check = {
        "time_from": time_from,
        "time_to": time_to
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }

    response_lesson = requests.post(url_lesson, data=json.dumps(data_check), headers=headers)
    if response_lesson.status_code == 200:
        await call.message.answer('Ваш урок успешно перенесён', reply_markup=start_kb)
    else:
        await call.message.answer('Что-то пошло не так', reply_markup=start_kb)

