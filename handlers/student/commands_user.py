import json
import os
from typing import List

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import MediaGroup

from keyboards.students.inlines import message_teacher
from loader import dp, db, bot
from models import Message, Link, Homework, User
from states import WriteTeacher


@dp.message_handler(text='/homework')
async def get_homework(message: types.Message):
    user = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    crm_user_id = user.crm_user_id
    homework = db.query(Homework).filter(Homework.crm_user_id == crm_user_id).first()
    photo = homework.photo
    text = homework.text
    if photo == 'У вас нет домашнего задания':
        await message.answer(f"Ваше домашнее задание:\n\n{text}")
    else:
        album = MediaGroup()
        photos = photo.split()
        for i in range(len(photos)):
            if i == 0:
                album.attach_photo(photo=photos[i], caption=f'Ваше домашнее задание:\n\n{text}')
            else:
                album.attach_photo(photo=photos[i])
        await message.answer_media_group(media=album)


@dp.message_handler(text='/lessonlink')
async def get_lesson_link(message: types.Message):
    user = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    crm_user_id = user.crm_user_id
    link = db.query(Link).filter(Link.crm_user_id == crm_user_id).first().text
    await message.answer(f"Ваша ссылка на урок:\n\n{link}")


def get_teacher_name(call):
    user = db.query(User).filter(User.tg_user_id == call.from_user.id).first()
    url_study = "https://selfree.s20.online/v2api/1/customer/index"
    data_check = {
        "id": user.crm_user_id
    }
    headers = {
        "X-ALFACRM-TOKEN": os.getenv("X-ALFACRM-TOKEN")
    }
    response_study = requests.post(url_study, data=json.dumps(data_check), headers=headers)
    name = response_study.json()['items'][0]['teacher_ids'][0]
    return name


@dp.message_handler(text='/sendtoteacher')
async def get_lesson_link(message: types.Message):
    await message.answer("Напишите сообщение учителю")
    await WriteTeacher.send_homework.set()


@dp.message_handler(content_types=['photo'], state=WriteTeacher.send_homework)
async def send_homework(message: types.Message, state: FSMContext, album: List[types.Message]):
    message_user = db.query(Message).filter(Message.tg_user_id == message.from_user.id).first()
    if message_user is None:
        message_user = Message()
        message_user.tg_user_id = message.from_user.id
        db.add(message_user)
        db.commit()
    message_user.text = message.caption
    message_user.photo = ' '.join(list(map(lambda x: x.photo[-1].file_id, album)))
    db.commit()
    await message.answer("Сообщение сохранено\n\nОтправить?", reply_markup=message_teacher)
    await state.finish()


@dp.message_handler(content_types=['text'], state=WriteTeacher.send_homework)
async def enter_homework_text(message: types.Message, state: FSMContext):
    message_user = db.query(Message).filter(Message.tg_user_id == message.from_user.id).first()
    if message_user is None:
        message_user = Message()
        message_user.tg_user_id = message.from_user.id
        db.add(message_user)
        db.commit()
    message_user.text = message.text
    message_user.photo = "Нет фото"
    db.commit()
    await message.answer("Сообщение сохранено\n\nОтправить?", reply_markup=message_teacher)
    await state.finish()


@dp.callback_query_handler(text='send_teacher')
async def send_teacher(call: types.CallbackQuery):
    teacher_name = get_teacher_name(call)
    teacher = db.query(User).filter(User.username == teacher_name, User.is_student == 0).first()
    if teacher is None:
        await call.message.answer("Преподаватель не зарегистрирован в боте")
    else:
        teacher_tg = teacher.tg_user_id
        message = db.query(Message).filter(Message.tg_user_id == call.from_user.id).first()
        photo = message.photo
        text = message.text
        if photo == 'Нет фото':
            await bot.send_message(teacher_tg, f"Вам сообщение от пользователя {call.from_user.full_name}"
                                               f"\n\nТекст:\n{text}")
        else:
            album = MediaGroup()
            photos = photo.split()
            for i in range(len(photos)):
                if i == 0:
                    album.attach_photo(photo=photos[i],
                                       caption=f"Вам сообщение от пользователя {call.from_user.full_name}"
                                               f"\n\nТекст:\n{text}")
                else:
                    album.attach_photo(photo=photos[i])
            await bot.send_media_group(chat_id=teacher_tg, media=album)
