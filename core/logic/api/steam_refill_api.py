
import aiohttp
import asyncio
import logging
from config import DESSLY_TOKEN, DEBUG_MODE
from utils.exceptions import API_ERRORS, BotError
from core.logic.repository.steam_refill_rep import create_steam_topup_order_db, update_order_status_db, delete_order_db
from core.logic.repository.user_rep import refund_balance


async def check_steam_login_api(login: str, amount: float):
    global DEBUG_MODE
    if DEBUG_MODE:
        return True
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
                error_text = API_ERRORS.get(error_code, 'Неизвестная ошибка API')
                logging.error(f'Ошибка от API: {error_text}')
                raise BotError(f'Ошибка от API: {error_text}')
        except Exception as e:
            logging.error(f'Ошибка сервиса API: {e}')
            raise BotError(f'Сервис временно недоступен, попробуйте позже!')

async def call_topup_api(login: str, amount: float):
    global DEBUG_MODE
    # проверка на дебаг мод(он для того чтоб проверять функции на работу, симуляция апишки)
    if DEBUG_MODE:
        return {"transaction_id": "MOCK_12345", "status": "success"}
    async with aiohttp.ClientSession() as session:
        url = 'https://desslyhub.com/api/v1/service/steamtopup/topup'
        payload = {'username': login, 'amount': amount}
        headers = {'apikey': DESSLY_TOKEN}         
        async with session.post(url, json=payload, headers=headers) as response:
            return await response.json()

async def create_steam_topup_order_api(customer_id, login: str, amount: float):
    order_in_db = await create_steam_topup_order_db(customer_id, "PENDING", "pending", amount)
    try:
        data = await call_topup_api(login, amount)
        if data.get('transaction_id'):
            await update_order_status_db(order_in_db.id, data.get('transaction_id'), data.get('status'))
            return {'uuid': data.get('transaction_id'), 'status': data.get('status')}
        error_code = data.get('error_code')
        error_text = API_ERRORS.get(error_code, 'Ошибка API')
        await refund_balance(customer_id, amount)
        await delete_order_db(order_in_db.id)
        raise BotError(f"Ошибка: {error_text}. Деньги возвращены на баланс.")
    except BotError:
        raise
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        await refund_balance(customer_id, amount)
        await delete_order_db(order_in_db.id)
        raise BotError("Ошибка связи с сервером. Деньги возвращены на баланс.")

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
                error_text = API_ERRORS.get(error_code, 'Неизвестная ошибка от API')
                logging.error(f'Ошибка от API: {error_text}')
                raise BotError(f'Ошибка от API: {error_text}')
        except Exception as e:
            logging.error(f'Ошибка сервиса в API: {e}')
            raise BotError(f'Сервис временно недоступен, попробуйте позже!: {e}')