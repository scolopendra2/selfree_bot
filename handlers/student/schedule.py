import datetime
import json
import locale
import os

import requests
from aiogram import types

from loader import dp, db, morph
from models import User
from keyboards.students import start_kb

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)


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


def get_left_lesson(user):  # функция для получения оставшихся оплаченных уроков(чтобы в Расписание были только они)
    url_study = "https://selfree.s20.online/v2api/1/customer/index"
    data_check = {
        "phone": user.phone
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    response_study = requests.post(url_study, data=json.dumps(data_check), headers=headers)
    return response_study.json()['items'][0]['paid_lesson_count']


@dp.message_handler(text='Расписание')
async def schedule(message: types.Message):
    check_in_table = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    if check_in_table is None:
        await message.answer("Вы не вошли в аккаунт", reply_markup=start_kb)
    else:
        user = check_in_table
        remains = get_left_lesson(user)
        items = get_items(user)[::-1][:remains]
        string = ''
        for item in items:
            number = items.index(item) + 1
            time_from_lesson = item['time_from']
            date_string, time_string = time_from_lesson.split(' ')
            date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
            month = date.strftime("%B")
            month_word = morph.parse(month)[0]
            month_name = month_word.inflect({"gent"}).word.capitalize()
            day_of_week = date.strftime("%A").capitalize()
            day = date_string.split('-')[2]
            time_to = ':'.join(item['time_to'].split()[1].split(':')[:2])
            time_from = ':'.join(item['time_from'].split()[1].split(':')[:2])
            string += (f'{number} Урок\n'
                       f'{day} {month_name} ({day_of_week})\n'
                       f'{time_from} - {time_to}\n\n')
        if string == '':
            string = 'У вас не осталось уроков'
    await message.answer(string, reply_markup=start_kb)
