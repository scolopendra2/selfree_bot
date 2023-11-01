from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from models import User, Homework
from states import SendHomework


@dp.message_handler(text='Отправить домашнее задание')
async def send_homework(message: types.Message):
    await message.answer("Введите ID студента:")
    await SendHomework.enter_id.set()


@dp.message_handler(content_types=['text'], state=SendHomework.enter_id)
async def enter_id(message: types.Message, state: FSMContext):
    user = db.query(User).filter(User.crm_user_id == message.text).first()
    if user is None:
        await message.answer("Пользователь с таким ID не зарегистрирован в боте")
    else:
        await state.update_data(enter_id=message.text)
        await message.answer("Введите текст домашнего задания:")
        await SendHomework.enter_homework.set()


@dp.message_handler(content_types=['photo'], state=SendHomework.enter_homework)
async def enter_homework_photo(message: types.Message, state: FSMContext, album: List[types.Message]):
    data = await state.get_data()
    homework = db.query(Homework).filter(Homework.crm_user_id == data['enter_id']).first()
    if homework is None:
        homework = Homework()
        homework.crm_user_id = data['enter_id']
        db.add(homework)
        db.commit()
    homework.text = message.caption
    homework.photo = ' '.join(list(map(lambda x: x.photo[-1].file_id, album)))
    db.commit()
    await message.answer("Домашка записана")
    user_tg_id = db.query(User).filter(User.crm_user_id == data['enter_id'], User.is_student == 1).first().tg_user_id
    await bot.send_message(chat_id=user_tg_id, text="Вам пришло новое домашнее задание, чтобы посмотреть"
                                                    "введите /homework")
    await state.finish()


@dp.message_handler(content_types=['text'], state=SendHomework.enter_homework)
async def enter_homework_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    homework = db.query(Homework).filter(Homework.crm_user_id == data['enter_id']).first()
    if homework is None:
        homework = Homework()
        homework.crm_user_id = data['enter_id']
        db.add(homework)
        db.commit()
    homework.text = message.text
    homework.photo = 'У вас нет домашнего задания'
    db.commit()
    await message.answer("Домашка записана")
    user_tg_id = db.query(User).filter(User.crm_user_id == data['enter_id'], User.is_student == 1).first().tg_user_id
    await bot.send_message(chat_id=user_tg_id, text="Вам пришло новое домашнее задание, чтобы посмотреть"
                                                    "введите /homework")
    await state.finish()
