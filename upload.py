import os
import asyncio
import logging
import df
from downloader import P 
from aiogram import Bot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pymongo
from pymongo import MongoClient
from db_map import Base, MediaIds
from aiohttp import ClientSession, TCPConnector

from config import TOKEN, MY_ID, DB_FILENAME
client = MongoClient("mongodb+srv://noema:658Vobisi@check.8n3yvam.mongodb.net/?retryWrites=true&w=majority")
db=client["Check"]
manhwa_data = db['manhwa']
manhwa_chapters = db['ex']
logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

engine = create_engine(f'sqlite:///{DB_FILENAME}')

if not os.path.isfile(f'./{DB_FILENAME}'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

bot = Bot(token=TOKEN)

import PyPDF2
import tempfile

async def compress_pdf(file):
    # Создаем временный файл для сжатого PDF
    temp_output = tempfile.NamedTemporaryFile(delete=False)

    try:
        pdf_writer = PyPDF2.PdfWriter()

        # Читаем входной PDF-файл
        pdf_reader = PyPDF2.PdfReader(file)

        # Итерируем по каждой странице входного PDF-файла
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]

            # Устанавливаем сжатие для страницы
            page.compress_content_streams()

            # Добавляем сжатую страницу в выходной PDF-файл
            pdf_writer.add_page(page)

        # Сохраняем сжатый PDF-файл во временный файл
        with open(temp_output.name, 'wb') as temp_file:
            pdf_writer.write(temp_file)

        # Возвращаем временный файл с сжатым PDF
        return temp_output.name

    except Exception as e:
        logging.error('Failed to compress PDF. Error: {}'.format(e))
        return None



async def uploadMediaFiles(name, path, method, file_attr):
    folder_path = path
    test_dict = dict()
    for filename in os.listdir(folder_path):
        if filename.startswith('.'):
            continue
        
        logging.info(f'Started processing {filename}')
        with open(os.path.join(folder_path, filename), 'rb') as file:
            new_path = os.path.join(folder_path, filename) 
            print(new_path)
            file_size_mb = os.path.getsize(new_path) / (1024 * 1024)
            print(file_size_mb)
            if file_size_mb > 50:
                # Сжимаем PDF-файл до размера меньше 50 МБ
                compressed_path = await compress_pdf(file)
                if compressed_path:
                    with open(compressed_path, 'rb') as compressed_file:
                        file_size_mb = os.path.getsize(compressed_path) / (1024 * 1024)
                        if file_size_mb < 50:
                            await asyncio.sleep(5)
                            msg = await method(MY_ID, compressed_file, disable_notification=True)
                else:
                    logging.error('Failed to compress PDF file: {}'.format(filename))
                    continue
            else:
                await asyncio.sleep(5)
                msg = await method(MY_ID, file, disable_notification=True)
            if file_size_mb < 50:
                if file_attr == 'photo':
                    file_id = msg.photo[-1].file_id
                else:
                    file_id = getattr(msg, file_attr).file_id
                session = Session()
                newItem = MediaIds(file_id=file_id, filename=filename)
                try:
                    session.add(newItem)
                    session.commit()
                    f=open('file.txt', 'a')
                except Exception as e:
                    logging.error(
                        'Couldn\'t upload {}. Error is {}'.format(filename, e))
                else:
                    filename = str(filename).replace('.pdf', '')
                    try:
                        df.add_chapters_to_storage(name, int(filename), file_id)
                    except ValueError as e:
                        print(f"Ошибка при вызове функции df.add_chapters_to_storage: {e}")

                    test_dict[filename] = file_id
                    f.write(filename+": '"+ file_id + "', " + "\n")
                finally:
                
                
                    session.close()
    df.add_manhwa_by_scraper(name, test_dict)
            
'''
loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(uploadMediaFiles('files', bot.send_document, 'document')),
]

wait_tasks = asyncio.wait(tasks)

loop.run_until_complete(wait_tasks)
loop.close()
Session.remove()

'''
