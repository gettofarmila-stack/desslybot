import asyncio
import logging
from aiogram import Router, Dispatcher, types, Bot
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = Router()
@router.error()
async def error_handler(event: types.ErrorEvent):
    logging.error(f"ОШИБКА: {event.exception}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logging.info('Бот запущен')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.info('Бот запущен')
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот выключен')