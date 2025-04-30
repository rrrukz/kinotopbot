from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import asyncpg

from data.config import ADMINS
from loader import dp, userdb, bot, kinodb
from states.state import User_delete, ReklamaState


# from states.select_user import Select_user

@dp.message_handler(commands="admin")
async def admin_commandlari(message:types.Message):
    await message.answer(
        "🔧 *ADMIN buyruqlari*\n"
        "---------------------\n"
        "🎬 *Kino uchun:*\n"
        "   ▪️ /kino_add\n"
        "   ▪️ /delete_movie\n"
        "   ▪️ /update_kino\n"
        "---------------------\n"
        "👤 *Userlar uchun:*\n"
        "   ▪️ /delete_user\n"
        "   ▪️ /userga_reklama\n"
        "---------------------\n"
        "📊 *Umumiy komandalar:*\n"
        "   ▪️ /reklama\n"
        "   ▪️ /statistika\n"
        "---------------------"
    )


# botdagi foydalanuvchilar soni
@dp.message_handler(commands="statistika")
async def count_user(message:types.Message):
    user_count= await userdb.count_users()
    kinolar = await kinodb.count_all_kinos()
    msg = "Botning statiskikasi\n"
    msg += f"Kinolar soni: {kinolar}\n"
    msg += f"Foydalanuvchilar soni :{user_count}"
    await bot.send_message(ADMINS[0], msg)

# reklama
@dp.message_handler(commands="reklama")
async def reklama_function(message:types.Message):
    users= await userdb.select_all_users()
    for user in users:
        await bot.send_message(user['telegram_id'],"Bot faol ishlamoqda  /start")

@dp.message_handler(commands="userga_reklama")
async def reklama_function(message:types.Message):
    await message.answer("Userni  ID-si kiriting: ")
    await ReklamaState.reklama.set()
@dp.message_handler(state=ReklamaState.reklama)
async def userga_reklama(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        id = int(message.text)
        user = await userdb.select_user(id=id)
        msg=f"reklama @{user['username']} ga yuborildi!"
        if user:
            await bot.send_message(user['telegram_id'],"Siz uchun maxsus reklama\n Hurmatli foydalanuvchi")
            await bot.send_message(ADMINS[0],msg)

        else:
            await message.answer("User  topilmadi")
    else:
        await message.answer("User ID-sini raqam sifatida yuboring: ")
    await state.finish()


# -------------------------------------------------------------------------------------------------

@dp.message_handler(commands="delete_user")
async def user_top(message:types.Message):
    await message.answer("Userni telegram ID-si kiriting: ")
    await User_delete.id.set()
@dp.message_handler(state= User_delete.id)
async def delete_user_by_id(message:types.Message,state:FSMContext):
    if message.text.isdigit():
        id = int(message.text)
        user = await userdb.select_user(id=id)
        if user:
            await userdb.delete_user(telegram_id=id)
            await message.answer("User o'chirildi")
        else:
            await message.answer("User topilmadi topilmadi")

    else:
        await message.answer("User ID-sini raqam sifatida yuboring: ")
    await state.finish()






# ------------------------------------------------+++++















































# @dp.message_handler(commands="delete")
# async def delete_user(message:types.Message):
#    await message.answer("siz ochirmoqchi bo'lgasn userni id- sini kiriting")
#    await Select_user.user_idisi.set()
# @dp.message_handler(state=Select_user.user_idisi)
# async def select_user(message:types.Message,state:FSMContext):
#     user=message.text
#     await state.update_data(
#         {"user":user}
#     )
#     await userdb.select_user()
#     data=await state.get_data()
#     user=data.get("user")
#     result=f"Foydalanuvchi{user} topildi\n"
#     await message.answer("Anniq o'chirmoqchimisiz ?")
#     await bot.send_message(ADMINS[0], result)
#     await state.finish()