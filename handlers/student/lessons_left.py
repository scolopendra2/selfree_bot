from aiogram import types
import os
import requests
import json

from loader import dp, db
from models import User


@dp.message_handler(text='Осталось уроков')
async def les_left(message: types.Message):
    check_in_table = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    if check_in_table is None:
        await message.answer("Вы не вошли в аккаунт")
    else:
        user = check_in_table
        url_study = "https://selfree.s20.online/v2api/1/customer/index"
        data_check = {
            "phone": user.phone
        }
        headers = {
            "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
        }
        response_study = requests.post(url_study, data=json.dumps(data_check), headers=headers)
        remains = response_study.json()['items'][0]['paid_lesson_count']
        await message.answer(f"Осталось уроков - {remains}")
