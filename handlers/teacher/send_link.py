from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from models import User, Link
from states import SendLink


@dp.message_handler(text='Прикрепить ссылку на урок')
async def send_link(message: types.Message):
    await message.answer("Введите ID студента")
    await SendLink.enter_id.set()


@dp.message_handler(content_types=['text'], state=SendLink.enter_id)
async def enter_id(message: types.Message, state: FSMContext):
    user = db.query(User).filter(User.crm_user_id == message.text).first()
    if user is None:
        await message.answer("Пользователь с таким ID не зарегистрирован в боте")
    else:
        await state.update_data(enter_id=message.text)
        await message.answer("Введите ссылку на урок:")
        await SendLink.enter_link.set()


@dp.message_handler(content_types=['text'], state=SendLink.enter_link)
async def enter_link(message: types.Message, state: FSMContext):
    data = await state.get_data()
    link = db.query(Link).filter(Link.crm_user_id == data['enter_id']).first()
    if link is not None:
        link.text = message.text
    else:
        link = Link()
        link.crm_user_id = data['enter_id']
        link.text = message.text
        db.add(link)
    db.commit()
    await message.answer("Ссылка добавлена")
    await state.finish()
