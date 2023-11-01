import json
import os

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import PAY_TOKEN
from loader import dp, bot, db
from models import User
from states import Pay


@dp.message_handler(text='/pay')
async def buy(message: types.Message):
    user = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    if user is None:
        await message.answer('Вы не вошли в аккаунт')
    else:
        await message.answer('Введите сумму платежа:')
        await Pay.data_pay.set()


@dp.message_handler(content_types=['text'], state=Pay.data_pay)
async def pay(message: types.Message, state: FSMContext):
    text = message.text
    if not text.isdigit():
        await message.answer('Это не число')
    else:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Оплата курсов',
            description='Тут описание курса',
            payload=f'Pay',
            provider_token=PAY_TOKEN,
            currency='rub',
            prices=[
                types.LabeledPrice(
                    label='Курсы',
                    amount=int(text) * 100
                )
            ],
            photo_url='https://kipmu.ru/wp-content/uploads/blkintfkt.jpg',
            photo_size=100
        )
        await state.finish()


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment_handler(message: types.Message):
    income = message.successful_payment.total_amount // 100
    print(income)
    user = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    crm_user_id = user.crm_user_id
    full_name = user.username
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    url = "https://selfree.s20.online/v2api/1/pay/create"
    data_check = {"branch_id": 1, "customer_id": crm_user_id, "document_date": "02.11.2023",
                  "income": income, "payer_name": full_name, "note": "Оплата через телеграмм бота",
                  "pay_type_id": 1,
                  "pay_account_id": 1}
    response = requests.post(url, data=json.dumps(data_check), headers=headers)
    if response.status_code == 200:
        await message.answer('Оплата прошла успешно')
    else:
        await message.answer('Что то пошло не так обратитесь к администратору')
