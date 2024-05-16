from downloader import MangaDownloader, P
import asyncio
import os 
from pathlib import Path
from toPDF import images_to_pdf
from upload import uploadMediaFiles
from config import TOKEN, MY_ID, DB_FILENAME
from htmlparse import propsParse

from aiogram import Bot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from db_map import Base, MediaIds
engine = create_engine(f'sqlite:///{DB_FILENAME}')

if not os.path.isfile(f'./{DB_FILENAME}'):
            Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
'''
1. проверка есть ли данная манга в бд. если да - скип
2. команда для отправки ссылки 
3
'''
import df
async def add_title_full(k):
    for i in k:
        bot = Bot(token=TOKEN)
        await bot.send_message('133886300', text = 'в работе')
        md = MangaDownloader(i)
        path=Path(__file__).parent
        await md.download(path=Path(__file__).parent)
        
        
        if P.name in df.available_manhwa():
              await bot.send_message('133886300', text = 'манхва уже имеется, мы ее пропускаем')
              print('манхва уже имеется, мы ее пропускаем')
        else:
            images_to_pdf(P.path)
            await propsParse(i)
            await uploadMediaFiles(P.name , P.path, bot.send_document, 'document')
        
        


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_title_full())
    loop.close()
    Session.remove()
    




