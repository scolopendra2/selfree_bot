async def on_startup(dp):
    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands

    await set_default_commands(dp)

    import asyncio
    from handlers.notifications.sborka import do_schedule
    asyncio.create_task(do_schedule(''))


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    from loader import Base, engine
    from handlers.notifications.update_token import get_x_alfacrm_token
    import os
    from middleware import AlbumMiddleware
    os.environ['X-ALFACRM-TOKEN'] = get_x_alfacrm_token()
    Base.metadata.create_all(engine)

    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, on_startup=on_startup)