from aiogram import types

from loader import dp, db
from models import User
from states import EnterNumber


@dp.message_handler(text='Выход')
async def exit_user(message: types.Message):
    user = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    db.delete(user)
    db.commit()
    await message.answer("Вы вышли. Введите номер телефона начиная с +7 📲",
                         reply_markup=types.ReplyKeyboardRemove())
    await EnterNumber.enter_number.set()
