from config import token_telegram
import asyncio

from aiogram  import Bot
from aiogram import Dispatcher

from app.handler import router






async def start():
    bot = Bot(token_telegram)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Бот выключен')


