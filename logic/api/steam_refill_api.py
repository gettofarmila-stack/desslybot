
import aiohttp
import asyncio
import logging
from config import DESSLY_TOKEN
from logic.repository.steam_refill_rep import create_steam_topup_order_db


API_ERRORS = {
    #ошибки транзакций
    -151: "Неверный ID транзакции.",
    -152: "Транзакция не найдена.",
    -153: "Не указан номер страницы.",

    # Ошибки сервиса гифтов
    -51: "Неверная ссылка для добавления в друзья.",
    -52: "Некорректный ID игры (App ID).",
    -53: "Информация об игре не найдена.",
    -54: "У пользователя нет основной игры (нужно для DLC).",
    -55: "Эта игра уже есть на аккаунте пользователя.",
    -56: "Не удалось добавить в друзья.",
    -57: "Указан неверный регион пользователя.",
    -58: "Регион получателя недоступен для отправки подарка.",
    -59: "Пользователь не добавил бота в друзья (или удалил его).",

    # Ошибки пополнения стим
    -100: "Неверный логин Steam. Проверь правильность написания!",
    
    # Дополнительные 
    -1: "Техническая ошибка сервиса. Попробуй позже.",
    -2: "У сервиса закончился баланс. Скоро пополним!",
    -3: "Неверная сумма пополнения.",
    -4: "Ошибка в структуре запроса.",
    -5: "Доступ запрещен (проблема с API-ключом).",

    # Ошибки курсов валют
    -120: "Некорректное значение валюты.",
    -121: "Данная валюта не поддерживается.",

    # Ошибки пополнения мобильных игр
    -200: "Мобильная игра не найдена.",
    -201: "Позиция в мобильной игре не найдена.",
    -202: "Вариант источника не найден.",

    # Ошибки ваучеров
    -300: "Ваучер не найден.",
    -301: "Ваучер недоступен."
}


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