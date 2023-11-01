import datetime
import json
import os

import requests
from aiogram import types

from keyboards.students import create_ikb_cancel
from loader import dp, db, bot
from models import User


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


@dp.message_handler(text='Отменить')
async def les_cancel(message: types.Message):
    check_in_table = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    if check_in_table is None:
        await message.answer("Вы не вошли в аккаунт")
    else:
        user = check_in_table
        remains = get_left_lesson(user)
        items = get_items(user)[::-1][:remains]
        await message.answer("Выберите урок, который хотите отменить", reply_markup=create_ikb_cancel(items))


def token_last_api():
    url = 'https://api.alfacrm.pro/v396/auth/login'

    headers = {
        'Accept': 'application/json',
        'X-APP-KEY': 'a7cf52fe0c0aae0d8770f8361610dab3',
        'Content-Type': 'application/json'
    }
    body = {
        'username': 'grisha.terteryan@mail.ru',
        'password': 'Selfreee2021'
    }
    return requests.post(url, data=json.dumps(body), headers=headers).json()['token']


@dp.callback_query_handler(lambda query: query.data.startswith('cancel_'))
async def cancel(call: types.CallbackQuery):
    id_lesson = call.data.split("_")[1]
    user = db.query(User).filter(User.tg_user_id == call.from_user.id).first()
    url_lesson = "https://selfree.s20.online/v2api/1/lesson/index"
    data_check = {
        "customer_id": user.crm_user_id,
        "status": 1,
        "id": id_lesson
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    response = requests.post(url_lesson, data=json.dumps(data_check), headers=headers)
    time_from = response.json()['items'][0]['time_from']
    target_date = datetime.datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')

    current_date = datetime.datetime.now()

    time_difference = target_date - current_date

    if time_difference.total_seconds() / 3600 < 5:
        await call.message.answer("Вы не можете отменить урок потому что до его начала осталось меньше 5 часов")
    else:
        url_for_cancel = f"https://api.alfacrm.pro/v396/lessons/lesson/{id_lesson}"
        data_cancel = {
            "property": "status",
            "value": "cancelled"
        }
        headers = {
            'Authorization': 'Bearer ' + token_last_api(),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-APP-KEY': 'a7cf52fe0c0aae0d8770f8361610dab3'
        }
        requests.patch(url_for_cancel, data=json.dumps(data_cancel), headers=headers)
        last_mes_id = call.message.message_id
        await bot.delete_message(call.from_user.id, last_mes_id)
        await call.message.answer("Ваш урок успешно отменён")
