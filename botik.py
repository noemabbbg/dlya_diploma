import asyncio
import logging
import random
from pathlib import Path
from typing import List, Union
import aiogram
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import (
    CallbackQuery,
    ChatActions,
    ContentType,
    File,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    KeyboardButton,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils import emoji, executor, helper
from aiogram.utils.markdown import bold, code, italic, pre, text
from audioop import add
from config import TOKEN
import keyboard as kb
import os
from aiogram_broadcaster import MessageBroadcaster, TextBroadcaster
from test2 import *



# привязка по жанрам. есть, но очень кривой и медленный код. 
# автообновление глав≠
# aergsthydtg
# handler криво работает. 



#уведомление о выходе новой главы 
#закладки 
#автообновление глав 




bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

class start_kb():
    keyboard = InlineKeyboardMarkup(row_width=2)
    manhwa_list_keyboard = InlineKeyboardMarkup(row_width=1)
    genres_list_keyboard = InlineKeyboardMarkup(row_width=1)

class add_new_manhwa(StatesGroup):
    name = State()
    picture = State()
    description = State()
    number_of_chapters = State()
    release_year = State()
    genres = State()
    manhwa_state = State()

class add_chapters_to_manhwa(StatesGroup):
    _id = State() # это будет id определнной произведения.
    filename = State()
    chapter_id = State()

class AlbumMiddleware(BaseMiddleware):
    album_data: dict = {}
    def __init__(self, latency: Union[int, float] = 0.01):   
        self.latency = latency
        super().__init__()
    async def on_process_message(self, message: types.Message, data: dict):
        if not message.media_group_id:
            return
        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler() 
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: types.Message, result: dict, data: dict):
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]




class AddChaptersToMangaParse(StatesGroup):
    __id = State()
    url = State () 

@dp.message_handler(commands='addchap', state = None)
#@dp.callback_query_handler(text = 'addchap', state = None)
async def add_manhwa_name(message: types.message):
    await add_chapters_to_manhwa._id.set()
    manhwa_ids =  added_manhwa =df.find_document_id(df.manhwa_data, {}, {'u_name':1, '_id':0, 'default_chap_name':1 })
    k = len(manhwa_ids)
    manhwa_ids_array = []
    await bot.send_message(message.from_user.id, text = 'выбери и скопируй название произведения, к которой нужно будет добавить новые главы \n')
    for i in range(0,k):
        manhwa_ids_array.append(str(manhwa_ids[i]).replace("'", ''))
        await bot.send_message(message.from_user.id, text = f'{manhwa_ids_array[i]}')
        i+=1

class Testt(StatesGroup):
    u_name = State() 



class NameNewChap():
    u_name = ''
@dp.message_handler(commands='addnewchap', state = None)
async def add_name(message: types.message):
    await Testt.u_name.set()
    await bot.send_message(message.from_user.id, text = "введи название добавленного тайтла, отправляй название, а потом главу пдфку" )

    
@dp.message_handler(state = Testt.u_name)
async def add_name(message: types.message, state = Testt.u_name):
    NameNewChap.u_name = message.text
    await state.finish()


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    
    document_file_id = message.document.file_id
    print(message.document.file_id)
    print(message.document.file_name)
    chapter_number = message.document.file_name.replace('.pdf', '')
    df.add_chapter_by_u_name(NameNewChap.u_name, chapter_number, document_file_id)

 
@dp.message_handler(commands='cancel', state = add_new_manhwa )
async def finish_state(message: types.message, state = add_new_manhwa):
    await state.finish()
@dp.message_handler(commands='cancel', state = add_chapters_to_manhwa )
async def finish_state(message: types.message,  state = add_chapters_to_manhwa):
    
    await state.finish()





@dp.message_handler(state = add_chapters_to_manhwa._id)
async def add_name(message: types.message, state = add_chapters_to_manhwa._id):
    async with state.proxy() as data:
        data['_id'] = message.text
        print(data['_id'])
    await add_chapters_to_manhwa.next()
    await message.reply('выгрузи')
    await message.reply('введи (номер главы), которую ты загружаешь. если глав несколько - вводи самую раннюю главу и присылай главы строго по порядку (пофикшу немного позже, пока костыль)')

@dp.message_handler(state = add_chapters_to_manhwa.filename)
async def add_name(message: types.message, state = add_chapters_to_manhwa.filename):
   
    async with state.proxy() as data:
        data['filename'] = message.text
        await message.reply(data['filename'])
    await add_chapters_to_manhwa.next()
    await message.reply('Теперь выгружай главы. ')


@dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY, state = add_chapters_to_manhwa.chapter_id)
async def handle_albums(message: types.Message, album: List[types.Message], state = add_chapters_to_manhwa):
    print( """This handler will receive a complete album of any type.""")
    """This handler will receive a complete album of any type."""
    media_group = types.MediaGroup()
    async with state.proxy() as data:
        for obj in album:
            if obj.photo:
                file_id = obj.photo[-1].file_id
            else:
             
                file_id = obj[obj.content_type].file_id
                
                file_info = await bot.get_file(obj[obj.content_type].file_id)
                filename = int(data['filename'])
                data['filename'] = filename+1
                await message.reply(filename)
               
            
           
                data['file_id'] = file_id
           
                await message.reply(str(data))
                # здесь передаем в бд.
                name = str(data['_id'])
                print('kjhgfcd')
                df.add_chapter_by_u_name(name, filename, file_id)
            try:
                # We can also add a caption to each file by specifying `"caption": "text"`
                media_group.attach({"media": file_id, "type": obj.content_type})
            except ValueError:
                return await message.answer("This/ type of album is not supported by aiogram.")
        await message.answer_media_group(media_group)
        await message.reply('Главы загружены, но это не точно ')
        await state.finish()

@dp.message_handler(commands=['adm'])
async def adm_panel(message: types.message):
    if message.from_user.id == 133886300:
        await bot.send_message(message.from_user.id, text = 'Панелька.', reply_markup = kb.adm_panel)
    else: 
        await bot.send_message(message.from_user.id, text = 'у тебя нет доступа братанчик, ну или есть🧐 ', reply_markup = kb.adm_panel)


@dp.message_handler(commands=['abobatest123'])
async def adm_panel(message: types.message):
    print(df.get_u_title_list())
    await add_title_full(df.get_u_title_list())




@dp.message_handler(commands=['ulistcheck'])
async def adm_panel(message: types.message):
   
    await bot.send_message(message.from_user.id, text = df.get_u_title_list())
    
    
        






#@dp.message_handler(commands = 'addtitle', state = None )
@dp.callback_query_handler(text ='addtitle', state = None )
async def first_step_to_add(message: types.message):
    
    await add_new_manhwa.name.set()
    await bot.send_message(message.from_user.id, text = 'впиши название произведения')

@dp.message_handler(state = add_new_manhwa.name)
async def add_name(message: types.message, state = add_new_manhwa.name):
    async with state.proxy() as data:
        data['name'] = message.text
    await add_new_manhwa.next()
    await message.reply('загрузи картинку произведения')


@dp.message_handler(content_types = ['photo'], state =add_new_manhwa.picture)
async def add_picture_to_manhwa(message: types.message, state: add_new_manhwa):
    
    async with state.proxy() as data:
        data['picture'] = message.photo[0].file_id
    await add_new_manhwa.next()
    await message.reply(" теперь введи описание")



@dp.message_handler(state = add_new_manhwa.description)
async def add_description(message: types.message, state = add_new_manhwa):
    async with state.proxy() as data:
        data['description'] = message.text
    await add_new_manhwa.next()
    await message.reply('введи общее количество глав')


@dp.message_handler(state = add_new_manhwa.number_of_chapters)
async def add_number_of_chapters(message: types.message, state = add_new_manhwa):
    async with state.proxy() as data:
        data['number_of_chapters'] = int(message.text)
    await add_new_manhwa.next()
    await message.reply(' теперь введи год релиза')


@dp.message_handler(state = add_new_manhwa.release_year)
async def add_release_year(message: types.message, state = add_new_manhwa):
    async with state.proxy() as data:
        data['release_year'] = int(message.text)
    await add_new_manhwa.next()
    await message.reply('теперь введи жанры, к которым относится тайтл, (одним соообщением через ,)')

@dp.message_handler(state = add_new_manhwa.genres)
async def add_release_year(message: types.message, state = add_new_manhwa):
    async with state.proxy() as data:
        data['genres'] = message.text
        genres = message.text 
        df.add_genre(genres)

    await add_new_manhwa.next()
    await message.reply('теперь введи статус тайтла (онгоинг/завершен/заморожен)')

@dp.message_handler(state = add_new_manhwa.manhwa_state)
async def add_manhwa_state(message: types.message, state = add_new_manhwa):
    async with state.proxy() as data:
        data['manhwa_state'] = message.text
    async with state.proxy() as data:
        await message.reply(str(data))
        
        name = str(data['name'])
        picture = str(data['picture'])
        description = str(data['description'])
        number_of_chapters = int(data['number_of_chapters'])
        release_year = int(data['release_year'])
        genres = str(data['genres'])
        manhwa_state = str(data['manhwa_state'])
        df.add_to_storage(name, picture, description, number_of_chapters,release_year,genres,manhwa_state)
    
    await state.finish()

@dp.message_handler(commands=['start'])
async def try1(message: types.message):
    user_id = message.from_user.id
    df.register_user(user_id)
    start_kb.keyboard = InlineKeyboardMarkup(row_width=2)
    
    added_manhwa = df.find_document(df.manhwa_data, {})
    buttons_list = []
    
    for i in added_manhwa:
        k = (str(i).replace('{', '').replace('}', '').replace("'", '').replace(":", '').replace("name", '').replace(" ", ''))
        buttons_list.append(i)
        button = InlineKeyboardButton(text = i, callback_data = i) # здесь мне нужно поймать выбранный callback юзера. мне нужно как то его записать в бд, вопрос как 
        #keyboard.insert(button)
    
    all_titles_button = InlineKeyboardButton(text = 'все тайтлы', callback_data='all_titles_button')
    genres_button = InlineKeyboardButton(text = 'жанры', callback_data='genres_list')

    start_kb.keyboard.insert(all_titles_button)
    start_kb.keyboard.insert(genres_button)



    @dp.callback_query_handler(text ='all_titles_button')
    async def genres_list(call: CallbackQuery):
        manhwa_list = df.u_available_manhwa()
        def_manhwa_list = df.available_manhwa()
        print(manhwa_list)
        back_to_main_menu = InlineKeyboardButton(text = '🔙', callback_data='back_to_main_menu')
        start_kb.manhwa_list_keyboard = InlineKeyboardMarkup(row_width=1)
        i = 0 
        while i<len(manhwa_list):
            if len(manhwa_list[i]) > 64:
                manhwa_list[i] = manhwa_list[i][:63]
            button =  InlineKeyboardButton(text = manhwa_list[i], callback_data = def_manhwa_list[i])
            start_kb.manhwa_list_keyboard.insert(button)
            i+=1
        start_kb.manhwa_list_keyboard.insert(back_to_main_menu)
        await bot.delete_message(call.from_user.id, call.message.message_id)
        
        await bot.send_message(call.from_user.id, text = 'все загруженные комиксы и манги', reply_markup=start_kb.manhwa_list_keyboard)


    @dp.callback_query_handler(text ='back_to_titles_list')
    async def back_to_titles_list(call: CallbackQuery):
         await bot.delete_message(call.from_user.id, call.message.message_id)
         await bot.send_message(call.from_user.id, text = 'все загруженные комиксы и манги', reply_markup=start_kb.manhwa_list_keyboard)


    @dp.callback_query_handler(text ='back_to_main_menu')
    async def back_to_main_menu(call: CallbackQuery):
        await bot.delete_message(call.from_user.id, call.message.message_id)
    
        await bot.send_message(call.from_user.id, text = 'Бот для чтения комиксов и книг в телеграмме! \n', reply_markup=start_kb.keyboard)



    @dp.callback_query_handler(text = buttons_list)
    async def process_video_command(call: CallbackQuery):
        manhwa_name = call.data 
        user_id = call.from_user.id
        df.selected_manhwa(manhwa_name, user_id)
        #await call.bot.send_message(call.from_user.id, text = f'ты попал в калбек {call.data}')
        await bot.delete_message(call.from_user.id, call.message.message_id)
        release_year = str(df.get_release_year(call.data)).replace("'", " ")
        number_of_chap = str(df.get_number_of_chap(call.data)).replace("'", " ")
        genre = str(df.get_manhwa_genres(call.data)).replace("['", " ").replace("']"," " )
        status = str(df.get_manhwa_state(call.data)).replace("'", " ")
        await bot.send_photo(call.from_user.id, 
        caption=f'*Описание: *{df.get_description(call.data)[0]} \n \n*Количество глав: * {number_of_chap}  \n*Год выпуска:* {release_year} \n\n *Жанры:* {genre} \n*Статус Тайтла: * {status}' ,photo=df.get_photo(call.data)[0], parse_mode="Markdown", reply_markup =kb.main_menu)
    await bot.send_message(message.from_user.id, text = 'Бот для чтения комиксов и книг в телеграмме! \n', reply_markup = start_kb.keyboard)

@dp.callback_query_handler(text ='genres_list')
async def genres_list(call: CallbackQuery):
    genres_list = df.available_genres()
    back_to_main_menu = InlineKeyboardButton(text = '🔙', callback_data='back_to_main_menu')
    
    start_kb.genres_list_keyboard = InlineKeyboardMarkup(row_width=1)
    i = 0 
    keyboard_text = []
    while i < len(genres_list):
        genre = genres_list[i]
        if genre not in keyboard_text:
            button = InlineKeyboardButton(text=genre, callback_data=genre)
            keyboard_text.append(genre)
            start_kb.genres_list_keyboard.insert(button)
        i += 1

    start_kb.genres_list_keyboard.insert(back_to_main_menu)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, text = 'доступные жанры', reply_markup=start_kb.genres_list_keyboard)


    @dp.callback_query_handler(text = genres_list)
    async def process_video_command(call: CallbackQuery):
        genre_name = call.data 
        accepted_manhwa = df.find_manhwa_genre(genre_name)
        u_accepted_manhwa  = df.u_find_manhwa_genre(genre_name)
        manhwa_in_genre = InlineKeyboardMarkup(row_width=1)
        i = 0 
        while i<len(accepted_manhwa):
            button =  InlineKeyboardButton(text = u_accepted_manhwa[i], callback_data = accepted_manhwa[i])
            manhwa_in_genre.insert(button)
            i+=1
        back_to_main_menu = InlineKeyboardButton(text = '🔙', callback_data='back_to_main_menu')
        manhwa_in_genre.insert(back_to_main_menu)
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, text = 'доступные тайтлы: ', reply_markup=manhwa_in_genre)
###
@dp.callback_query_handler(text = 'start_read')
async def start_reading(call: CallbackQuery):
  manhwa_name = df.get_selected_manhwa(call.from_user.id)
  df.update_selected_chapter(call.from_user.id, 1)
  try:
    await call.bot.send_document(call.from_user.id, document=df.get_chapters(manhwa_name, 1), reply_markup=kb.next_chapterKB) 
  except:
    await call.bot.send_message(call.from_user.id, text = 'Главы еще не добавлены в систему', reply_markup=back_to_main_menu)
# клаву с менюшкой + калбек на выдачу глав сделать
back_to_main_menu = InlineKeyboardMarkup(row_width=1)
back_to_menu = InlineKeyboardButton(text = '🔙', callback_data='back_to_main_menu')
back_to_main_menu.insert(back_to_menu)


#user_list = []

'''
@dp.message_handler(commands=['manylink'])
async def get_link(message: types.Message):
    await bot.send_message(message.from_user.id, text = 'Привет! Проверка функции автоматического добавления произведения с мангалиба :) Присылай в ответ ссылку тайтла, который хочешь добавить в формате: https://mangalib.me/kod-giass/v5/c18?ui=156163&page=1 ')
    @dp.message_handler()
    async def get_link(message: types.Message):
        urls = message.text
        print(urls)
        for url in urls:
            df.add_u_title_list(url)
        
       # user_list.append(str(message.text))
       # print(user_list)
        await message.reply('Ссылку получил, спасибо!')
'''
@dp.message_handler(commands=['onelink'])
async def get_link(message: types.Message):
    await bot.send_message(message.from_user.id, text = 'Проверка функции автоматического добавления комикса с мангалиба :) В ответ прикрепляй ссылку тайтла, который хочешь добавить в формате: https://mangalib.me/kod-giass/v5/c18?ui=156163&page=1.')
    @dp.message_handler()
    async def get_link(message: types.Message):
        df.add_u_title_list(message.text)
       # user_list.append(str(message.text))
       # print(user_list)
        await message.reply('Ссылку получил, спасибо!')

@dp.callback_query_handler(text = 'start_modify_read')
async def start_reading(call: CallbackQuery):
  manhwa_name = df.get_selected_manhwa(call.from_user.id)
  await call.bot.send_message(call.from_user.id, text = f'Напиши номер главы', reply_markup=back_to_main_menu)
  
  @dp.message_handler()
  async def change_chapter(message: types.Message):
    manhwa_name = df.get_selected_manhwa(message.from_user.id)
    try: 
        new_chapter = int(message.text)
    except: 
        await  call.bot.send_message(message.from_user.id, text = 'главу не удалось найти, попробуй снова')
    df.update_selected_chapter(message.from_user.id, new_chapter)
    new_chapter = int((df.selected_chapter(message.from_user.id))[0])
    try: 
    
        await call.bot.send_document(message.from_user.id, document=df.get_chapters(manhwa_name, new_chapter), reply_markup=kb.next_chapterKB) 
    except: 
        await call.bot.send_message(message.from_user.id, text = 'главу не удалось найти, попробуй снова')



@dp.callback_query_handler(text = 'next_chapter') # работает, но надо переписать по человечески.
async def next_chapter(call: CallbackQuery):
    k = int(df.selected_chapter(call.from_user.id)[0])

    new_chapter = df.update_selected_chapter(call.from_user.id, k+1)
    new_chapter = int((df.selected_chapter(call.from_user.id))[0])
    
    manhwa_name = df.get_selected_manhwa(call.from_user.id)
    
    try: 
         await call.bot.send_document(call.from_user.id, document=df.get_chapters(manhwa_name, new_chapter), reply_markup=kb.next_chapterKB)
    except:
        await call.bot.send_message(call.from_user.id, text = 'кажется новых глав еще нет', reply_markup=kb.main_menu)
        



if __name__ == "__main__":
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)

