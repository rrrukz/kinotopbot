from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from utils.db_api.kino_db import KinoDatabase
from utils.db_api.postgre_sql import Database
from utils.db_api.users import UserDatabase

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db=Database()
userdb=UserDatabase()
kinodb=KinoDatabase()