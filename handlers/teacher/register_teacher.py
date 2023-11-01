from aiogram import types
from models import User
import json
import requests
import os
from loader import dp, db
from keyboards import teacher_kb

@dp.message_handler(lambda message: message.text.startswith('teacher '))
async def start_teacher(message: types.Message):
    text = message.text.split()[1]
    url_teacher = "https://selfree.s20.online/v2api/1/teacher/index"
    data_check = {
        "phone": text
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    if not text.startswith("+7"):
        await message.answer("""Номер телефона не начинается с +7""")
    elif len(text) != 12:
        await message.answer("""В номере телефона не может быть больше 11 цифр""")
    else:
        response_teacher = requests.post(url_teacher, data=json.dumps(data_check), headers=headers)
        if len(response_teacher.json()['items']) == 0:
            await message.answer("Такого номера нет в базе учителей SELFREE 🤷‍♂️")
        else:
            check = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
            if check is not None:
                db.delete(check)
                db.commit()
            name_user = response_teacher.json()['items'][0]["name"]
            user = User()
            user.username = name_user
            user.is_student = False
            user.tg_user_id = message.from_user.id
            user.crm_user_id = response_teacher.json()['items'][0]['id']
            user.phone = text
            db.add(user)
            db.commit()
            await message.answer(f"""Приветствую, {name_user} 🖐 
Здесь вы будете получать уведомления об изменённых занятиях в вашем расписании!""", reply_markup=teacher_kb)
