import json
import os

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from models import User
from states import EnterNumber
from keyboards.students import start_kb


@dp.message_handler(text='/start')
async def start(message: types.Message):
    await message.answer("""Дорогой студент ☺️! 

 Я telegramm бот 🤖, который поможет тебе следить за твоими занятиями 😏 ))) 

 Чтобы авторизоваться, введи свой номер телефона начиная с +7.""")
    await EnterNumber.enter_number.set()


@dp.message_handler(content_types=['text'], state=EnterNumber.enter_number)
async def check_number(message: types.Message, state: FSMContext):
    url_study = "https://selfree.s20.online/v2api/1/customer/index"
    data_check = {
        "phone": message.text
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    if not message.text.startswith("+7"):
        await message.answer("""Номер телефона не начинается с +7""")
    elif len(message.text) != 12:
        await message.answer("""В номере телефона не может быть больше 11 цифр""")
    else:
        response_study = requests.post(url_study, data=json.dumps(data_check), headers=headers)
        if len(response_study.json()['items']) == 0:
            await message.answer("Такого номера нет в базе студентов SELFREE 🤷‍♂️")
        else:
            check = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
            if check is not None:
                db.delete(check)
                db.commit()
            name_user = response_study.json()['items'][0]["name"]
            user = User()
            user.username = name_user
            user.tg_user_id = message.from_user.id
            user.crm_user_id = response_study.json()['items'][0]['id']
            user.phone = message.text
            db.add(user)
            db.commit()
            await message.answer(f"""{name_user}, рады приветствовать Вас на обучении 👋

🤖 Благодаря данному боту:
✔️ вы можете изучать уроки;
✔️ смотреть расписание и его корректировать;
✔️ выполнять домашние задания;
✔️ производить оплату.

Желаем вам успехов в обучении Selfree! 🚀""", reply_markup=start_kb)
        await state.finish()
