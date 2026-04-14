import aiohttp
import logging
from config import PROJECT_UUID
from utils.utils import generate_sign
from utils.exceptions import BotError
import json

async def create_payment_api(amount, order_id):
    url = 'https://api.2328.io/api/v1/payment'
    data = {
        "amount": f"{amount:.2f}",
        "currency": "USD",
        "order_id": str(order_id),
        'url_callback': 'https://webhook.site/06b7f86a-ccc3-45df-bc87-80cc0b7b9ad8'
    }
    json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    sign = generate_sign(data)
    headers = {'Content-Type': 'application/json', 'project': PROJECT_UUID, 'sign': sign}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                data=json_str.encode('utf-8'),
                headers=headers
            ) as response:
                resp_data = await response.json()
                if resp_data.get('state') == 0:
                    return resp_data['result']
                raise BotError(f"Ошибка: {resp_data}")
    except Exception as e:
        logging.error(f"Ошибка create_payment_api: {e}")
        raise BotError("Ошибка АПИ платёжки")
    
