from logic.api.steam_refill_api import check_steam_login_api, create_steam_topup_order_api, checking_exchange_rate_api
from utils.exceptions import BotError

async def create_steam_topup_order(customer_id, login: str, amount: float):
    if amount < 0.1:
        raise BotError('Слишком маленькая сумма пополнения!')
    await check_steam_login_api(login, amount)
    return await create_steam_topup_order_api(customer_id=customer_id, login=login, amount=amount)

async def check_exchange_rate(amount, currency):
    exchange_rate = await checking_exchange_rate_api(currency=currency)
    if exchange_rate == 1:
        total_sum = amount
    else:
        total_sum = (amount / exchange_rate) * 1.02
    return round(total_sum, 2)