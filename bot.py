import asyncio
import logging
from aiogram import Router, Dispatcher, types, Bot
from handlers import common, steam_refill, steam_gifts, error, vouchers, profile
from config import BOT_TOKEN
from database.models import init_models
from utils.get_cache import on_startup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = Router()
@router.error()
async def error_handler(event: types.ErrorEvent):
    logging.error(f"ОШИБКА: {event.exception}")

async def main():
    await init_models()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(error.router)
    dp.include_routers(router, common.router, steam_refill.router, steam_gifts.router, vouchers.router, profile.router)

    dp.startup.register(on_startup)
    logging.info('Бот запущен')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.info('Бот запущен')
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот выключен')