
import logging
import aiohttp
import asyncio
from config import DESSLY_TOKEN
from utils.exceptions import API_ERRORS, BotError


async def get_vouchers_api():
    async with aiohttp.ClientSession() as session:
        url = 'https://desslyhub.com/api/v1/service/voucher/products'
        headers = {'apikey': DESSLY_TOKEN}
        async with session.get(url, headers=headers) as response:
            raw_data = await response.json()
            if raw_data.get('products'):
                return raw_data
            error_text = API_ERRORS.get(raw_data.get('error_code'), 'Unknown API Error')
            raise Exception(f'API Dessly вернуло ошибку: {error_text}')
        
async def get_voucher_info_api(id):
    async with aiohttp.ClientSession() as session:
        try:
            url = f'https://desslyhub.com/api/v1/service/voucher/products/{id}'
            headers = {'apikey': DESSLY_TOKEN}
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                if data.get('name'):
                    return data
                error_text = API_ERRORS.get(data.get('error_code'), 'Unkown API Error')
                logging.info(f'Ошибка от API: {error_text}')
                raise BotError(f'Ошибка от API: {error_text}')
        except BotError:
            raise
        except Exception as e:
            logging.error(f'Ошибка от сервиса API: {e}')
            raise BotError(f'Ошибка связи с сервером, напишите в поддержку если ошибка повторится')