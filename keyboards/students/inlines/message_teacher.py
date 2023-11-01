from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

message_teacher = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [InlineKeyboardButton(text='Отправить',
                                                                 callback_data="send_teacher")]
                                       ])
