
import logging
import aiohttp
import asyncio
from config import DESSLY_TOKEN, DEBUG_MODE
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
                logging.error(f'Ошибка от API: {error_text}')
                raise BotError(f'Ошибка от API: {error_text}')
        except BotError:
            raise
        except Exception as e:
            logging.error(f'Ошибка от сервиса API: {e}')
            raise BotError(f'Ошибка связи с сервером, напишите в поддержку если ошибка повторится')
        
async def buy_voucher_api(voucher_id, var_id):
    global DEBUG_MODE
    if DEBUG_MODE:
        return {"transaction_uuid": "97945ca7-312c-4cc9-97fb-f27d07b81bff", "status": "success", "vouchers": [{"serialNumber": "123456", "pin": "zauvutfeq2wq237dm", "expiration": "2006-01-02 15:04:05"}]}
    async with aiohttp.ClientSession() as session:
        try:
            url = 'https://desslyhub.com/api/v1/service/voucher/buy'
            payload = {'root_id': voucher_id, 'variant_id': var_id}
            headers = {'apikey': DESSLY_TOKEN, 'content-type': 'application/json'}
            async with session.post(url, json=payload, headers=headers) as response:
                data = await response.json()
                if data.get('status'):
                    return data
                error_code = data.get('error_code')
                error_text = API_ERRORS.get(error_code, 'Unkown API Error')
                logging.error(f'Ошибка от API: {error_text} под {error_code}')
                raise BotError(f'Ошибка от API: {error_text}')
        except BotError:
            raise
        except Exception as e:
            logging.error(f'Ошибка от сервиса API: {e}')
            raise BotError(f'Ошибка связи с сервером, напишите в поддержку если ошибка повторится')