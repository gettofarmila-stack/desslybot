import aiohttp
import asyncio
import logging
from config import DESSLY_TOKEN, API_ERRORS


async def get_games_list():
    async with aiohttp.ClientSession() as session:
        try:
            url = 'https://desslyhub.com/api/v1/service/steamgift/games'
            header = {'apikey': DESSLY_TOKEN}
            async with session.get(url, headers=header) as response:
                raw_data = await response.json()
                games = raw_data.get('games') if isinstance(raw_data, dict) else raw_data
                if isinstance(games, list):
                    formatted_games = [{'name': game.get('name'), 'appid': game.get('appid')} for game in games if game.get('appid')]
                    return formatted_games
                error_code = raw_data.get('error_code')
                if error_code:
                    error_text = API_ERRORS.get(error_code)
                    logging.warning(f'Ошибка ({error_code}): {error_text}')
                    return False
                logging.warning('Неизвестная ошибка от API!')
                return False
        except Exception as e:
            logging.warning(f'Ошибка системы: {e}')
            return False
        