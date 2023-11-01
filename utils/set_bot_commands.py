from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Начать'),
        types.BotCommand('homework', "Домашнее задание"),
        types.BotCommand('lessonlink', "Ссылка на урок"),
        types.BotCommand('pay', "Пополнить баланс")
    ])
