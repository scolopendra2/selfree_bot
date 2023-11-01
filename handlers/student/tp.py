from aiogram import types

from keyboards.students.inlines import ikb_tp
from loader import dp


@dp.message_handler(text='Тех. Поддержка')
async def tp(message: types.Message):
    await message.answer(
        "Если у вас вопросы или какие-то предложения, можете написать нашему сотруднику "
        "https://t.me/selfree_call_center_bot",
        reply_markup=ikb_tp)
