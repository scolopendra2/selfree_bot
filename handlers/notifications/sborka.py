import asyncio

import aioschedule

from loader import dp

from .update_token import update
from .check_paid_lesson import paid_lesson


@dp.message_handler()
async def do_schedule(mes):
    aioschedule.every(13).minutes.do(update)
    aioschedule.every().day.at('12:28').do(paid_lesson)
    aioschedule.every().day.at('12:30').do(paid_lesson)
    aioschedule.every().day.at('12:32').do(paid_lesson)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
