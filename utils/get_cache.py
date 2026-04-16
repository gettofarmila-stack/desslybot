import json
import asyncio
import logging
import time
from core.logic.api.steam_gift_api import get_games_list
from core.logic.api.voucher_api import get_vouchers_api

GAMES_CACHE = []
VOUCHERS_CACHE = []

async def update_games_task(interval=3600):
    global GAMES_CACHE
    while True:
        logging.info('Обновляю список игр...')
        games = await get_games_list()
        if games:
            GAMES_CACHE.clear()
            GAMES_CACHE.extend(games)
            logging.info(f'Успешно загружено {len(games)} игр!')
        else:
            logging.error('При обновлении списка игр что-то пошло не так, попробую ещё раз...')
            await asyncio.sleep(10)
            continue
        await asyncio.sleep(interval)

async def update_vouchers_task(interval=3600):
    global VOUCHERS_CACHE
    while True:
        try:
            logging.info('Запрашиваю список ваучеров...')
            vouchers = await get_vouchers_api()
            products = vouchers.get('products', [])
            if products:
                VOUCHERS_CACHE.clear()
                VOUCHERS_CACHE.extend(products)
                logging.info(f'Загружено {len(products)} ваучеров')
                await asyncio.sleep(interval)
        except Exception as e:
            logging.error(f'При загрузке ваучеров произошла ошибка: {e}... Пробую снова')
            await asyncio.sleep(10)

async def on_startup(bot):
    asyncio.create_task(update_games_task())
    asyncio.create_task(update_vouchers_task())
    logging.info('Фоновая задача обновления игр запущена')