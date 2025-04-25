from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import asyncpg

from data.config import ADMINS
from loader import dp, userdb, bot


# botdagi foydalanuvchilar soni
@dp.message_handler(commands="count")
async def count_user(message:types.Message):
    user_count= await userdb.count_users()
    msg="botdagi ja'mi foydalanuvchilar soni\n"
    msg+=f"{user_count} ta \n"
    await bot.send_message(ADMINS[0],msg)

# reklama
@dp.message_handler(commands="reklama")
async def reklama_function(message:types.Message):
    users= await userdb.select_all_users()
    for user in users:
        await bot.send_message(user['telegram_id'],"Bu reklama")