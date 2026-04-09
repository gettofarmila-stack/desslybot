
import aiohttp
import asyncio
import logging
from config import DESSLY_TOKEN, API_ERRORS
from logic.repository.steam_refill_rep import create_steam_topup_order_db


async def check_steam_login_api(login: str, amount: float):
    async with aiohttp.ClientSession() as session:
        try:
            url = 'https://desslyhub.com/api/v1/service/steamtopup/check_login'
            payload = {'username': login, 'amount': amount}
            headers = {'apikey': DESSLY_TOKEN, 'content-type': 'application/json'}
            async with session.post(url, json=payload, headers=headers) as response:
                data = await response.json()
                if data.get('can_refill') is True:
                    return True
                error_code = data.get('error_code')
                if error_code:
                    error_text = API_ERRORS.get(error_code)
                    logging.warning(f'Ошибка ({error_code}): {error_text}')
                    return False
                logging.warning('Неизвестный ответ от API')
                return False
        except Exception as e:
            logging.warning(f'Ошибка сети: {e}')
            return False

async def create_steam_topup_order_api(customer_id, login: str, amount: float):
    async with aiohttp.ClientSession() as session:
        try:
            url = 'https://desslyhub.com/api/v1/service/steamtopup/topup'
            payload = {'username': login, 'amount': amount}
            headers = {'apikey': DESSLY_TOKEN, 'content-type': 'application/json'}
            async with session.post(url, json=payload, headers=headers) as response:
                data = await response.json()
                if data.get('transaction_id') and data.get('status'):
                    try:
                        order_id = data.get('transaction_id')
                        result = await create_steam_topup_order_db(customer_id=customer_id, transaction_id=order_id, status=data.get('status'), amount=amount)
                        if isinstance(result, str):
                            return result
                        return(f'Заказ №{order_id} успешно создан!')
                    except Exception:
                        return(f'При создании заказа №{order_id} в базе данных что-то пошло не так... Пожалуйста, обратитесь в поддержку.')
                error_code = data.get('error_code')
                if error_code:
                    error_text = API_ERRORS.get(error_code)
                    logging.warning(f'Ошибка ({error_code}): {error_text}')
                    return False
                logging.warning('Неизвестный ответ от API')
                return False
        except Exception as e:
            logging.warning(f'Ошибка сети: {e}')
            return False

async def checking_exchange_rate_api(currency):
    if currency == '1':
        return 1
    async with aiohttp.ClientSession() as session:
        try:
            url = f'https://desslyhub.com/api/v1/exchange_rate/steam/{currency}'
            headers = {'apikey': DESSLY_TOKEN}
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                if data.get('exchange_rate'):
                    return data.get('exchange_rate')
                error_code = data.get('error_code')
                if error_code:
                    error_text = API_ERRORS.get(error_code)
                    logging.warning(f'Ошибка ({error_code}): {error_text}')
                    return False
                logging.warning('Неизвестный ответ от API')
                return False
        except Exception as e:
            logging.warning(f'Ошибка сети: {e}')
            return False