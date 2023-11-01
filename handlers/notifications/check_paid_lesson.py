from loader import db, bot
from models import User
import requests
import os
import json


async def paid_lesson():
    all_user = db.query(User).all()
    for user in all_user:
        url_study = "https://selfree.s20.online/v2api/1/customer/index"
        data_check = {
            "phone": user.phone
        }
        headers = {
            "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
        }
        response_study = requests.post(url_study, data=json.dumps(data_check), headers=headers)
        remains = response_study.json()['items'][0]['paid_lesson_count']
        if remains == 1:
            await bot.send_message(chat_id=user.tg_user_id, text="У вас остался 1 оплаченный урок")
        if remains == 0:
            await bot.send_message(chat_id=user.tg_user_id, text="У вас не осталось оплаченных уроков")
