import aiohttp
import asyncio
import logging
from config import DESSLY_TOKEN
from utils.exceptions import API_ERRORS, BotError


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
        
async def get_game_info_api(app_id):
    async with aiohttp.ClientSession() as session:
        try:
            url = f'https://desslyhub.com/api/v1/service/steamgift/games/{app_id}'
            header = {'apikey': DESSLY_TOKEN}
            async with session.get(url, headers=header) as response:
                raw_data = await response.json()
                if raw_data.get('game'):
                    return(raw_data.get('game'))
                error_code = raw_data.get('error_code')
                if error_code:
                    error_text = API_ERRORS.get(error_code)
                    logging.warning(f'Ошибка ({error_code}): {error_text}')
                    return False
                logging.warning('Неизвестная ошибка от API')
                return False
        except Exception as e:
            logging.warning(f'Ошибка системы: {e}')
            return False
        
async def create_gift_order_api(steam_link, region, package_id):
    async with aiohttp.ClientSession() as session:
        try:
            url = 'https://desslyhub.com/api/v1/service/steamgift/sendgames'
            payload = {'invite_url': steam_link, 'package_id': package_id, 'region': region}
            headers = {'apikey': DESSLY_TOKEN, 'content-type': 'application/json'}
            async with session.post(url, json=payload, headers=headers) as response:
                raw_data = await response.json()
                if raw_data.get('transaction_id'):
                    return raw_data
                error_code = raw_data.get('error_code')
                error_text = API_ERRORS.get(error_code, 'Неизвестная ошибка API')
                raise BotError(f'Ошибка API: {error_text}')
        except Exception as e:
            logging.error(f'Системная ошибка API: {e}')
            raise BotError('Сервис временно недоступен, попробуйте позже!')