from logic.api.trade_api import check_steam_login_api, create_steam_topup_order_api, checking_exchange_rate_api

async def create_steam_topup_order(customer_id, login: str, amount: int):
    if amount < 0.1:
        return 'Слишком маленькая сумма!'
    resp = await check_steam_login_api(login, amount)
    if resp is False:
        return 'Не удалось пополнить, юзер не найден или сервис не доступен'
    response = await create_steam_topup_order_api(customer_id=customer_id, login=login, amount=amount)
    if response is False:
        return 'Ошибка на стороне API, обратитесь в поддержку или попробуйте позже'
    return response

async def check_exchange_rate(amount, currency):
    exchange_rate = await checking_exchange_rate_api(currency=currency)
    if exchange_rate is False:
        return False
    total_sum = amount / (exchange_rate * 1.02)
    return round(total_sum, 2)