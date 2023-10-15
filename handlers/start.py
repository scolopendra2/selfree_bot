from aiogram import types

from loader import dp


@dp.message_handler(text='/start')
async def start(message: types.Message):
    await message.answer('Я бот')
