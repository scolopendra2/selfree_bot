import pymorphy2
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

data = {
    "api_key": config.API_KEY,
    "email": config.EMAIL
}

engine = create_engine(
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@"
    f"{config.MYSQL_HOST}:{config.MYSQL_PORT}/selfree_tg_bot_2"
)

local_session = sessionmaker(autoflush=False,
                             autocommit=False, bind=engine)

db = local_session()

Base = declarative_base()

morph = pymorphy2.MorphAnalyzer()
