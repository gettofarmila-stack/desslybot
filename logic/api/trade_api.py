
import aiohttp
import asyncio
import logging
from config import DESSLY_TOKEN

API_ERRORS = {
    -1: "Техническая ошибка на стороне сервиса. Попробуй позже.",
    -2: "Баланс пуст.",
    -3: "Неверная сумма пополнения.",
    -4:	"Неправильный орган запроса",
    -5: "Проверь АПИ ключ, доступ запрещён."
}

async def check_steam_login_api(login: str, amount: int):
    async with aiohttp.ClientSession() as session:
        try:
            url = 'https://desslyhub.com/api/v1/service/steamtopup/check_login'
            payload = {
                'username': login,
                'amount': amount
            }
            headers = {
                'apikey': DESSLY_TOKEN,
                'content-type': 'application/json'
            }
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
