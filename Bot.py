import asyncio
#import logging
from app.handlers import router
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.db import db_start

TOKEN_API = "7896545661:AAHmHZ18r-gf3__fwo8-WetOHXcLElpw0lQ"

bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

async def main():
    await db_start()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')