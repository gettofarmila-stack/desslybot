import json
import asyncio
import logging
import time
from logic.api.steam_gift_api import get_games_list

GAMES_CACHE = []

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

async def on_startup(bot):
    asyncio.create_task(update_games_task())
    logging.info('Фоновая задача обновления игр запущена')