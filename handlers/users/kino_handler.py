from email.policy import default
from token import AWAIT

from states.state import KinoState, Update
from loader import dp,bot,kinodb
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
@dp.message_handler(commands="kino_add")
async def kino_add_function(message:types.Message):
    await message.answer("Kinoni yuboring: ")
    await KinoState.kino.set()

@dp.message_handler(state=KinoState.kino,content_types=types.ContentTypes.VIDEO)
async def kino_add_content(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['file_id']=message.video.file_id
        data['caption']=message.caption or 'Kino'

    await message.answer("Kino uchun kod kiriting: ")
    await KinoState.kod.set()

@dp.message_handler(state=KinoState.kod,content_types=types.ContentTypes.TEXT)
async def kino_add_kod(message:types.Message,state:FSMContext):
    try:
        post_id=int(message.text)
        async with state.proxy() as data:
            data['post_id']=post_id
            await kinodb.add_kino(post_id=data['post_id'],
                                  file_id=data['file_id'],
                                  caption=data['caption'])
        await message.answer("Kino muvaffaqiyatli qo'shildi.")
        await state.finish()
    except ValueError:
        await message.answer("Kino uchun kodni raqam sifatida kiriting")




# kinoni topish kod boyicha:
@dp.message_handler(lambda message :message.text.isdigit())
async def kino_top(message:types.Message):
    if message.text.isdigit():
        post_id=int(message.text)
        data=await kinodb.get_kino_by_post_id(post_id=post_id)
        if data:
            try:
                kinodb.increment_kino_views(post_id=post_id)
                await bot.send_video(chat_id=message.from_user.id,
                                 video=data['file_id'],
                                 caption=f"{data['caption']}\n\nYanada ko'proq kinolar uchun: @MENU_ubot")
            except:
                await message.answer("Kino topildi yuborishda xatolik qayta urunib koring")
        else:
            await message.answer("Kino topilmadi")

    else:
        await message.answer("Kino uchun kodni raqam sifatida yuboring: ")




@dp.message_handler(commands="delete_movie")
async def kino_top(message:types.Message):
    await message.answer("Kinoni kodini kiriting: ")
    await KinoState.delete_movie.set()
@dp.message_handler(state=KinoState.delete_movie)
async def delete_movie_by_post_id(message:types.Message,state:FSMContext):
    if message.text.isdigit():
        post_id = int(message.text)
        data = await kinodb.get_kino_by_post_id(post_id=post_id)
        if data:
                await kinodb.delete_movie(post_id=post_id)
                await message.answer("kino muvofaqiyatli o'chirildi")
        else:
            await message.answer("Kino topilmadi")

    else:
        await message.answer("Kino uchun kodni raqam sifatida yuboring: ")
    await state.finish()


@dp.message_handler(commands="update_kino")
async def kinoni_yangilash(message:types.Message,state:FSMContext):
    await message.answer("Siz update qilmoqchi bo'lgan kinoni post_id sini kiriting")
    await Update.update_kino.set()
@dp.message_handler(state=Update.update_kino)
async def kinoni_yangilash(message:types.Message,state:FSMContext):
    if message.text.isdigit():
        post_id = int(message.text)
        data = await kinodb.get_kino_by_post_id(post_id=post_id)
        if data:
            await kinodb.update_kino_caption(post_id=post_id,new_caption="Caption yangilandi👇")
            await message.answer("kino muvofaqiyatli yangilandi")
        else:
            await message.answer("Kino topilmadi")

    else:
        await message.answer("Kino uchun kodni raqam sifatida yuboring: ")
    await state.finish()






