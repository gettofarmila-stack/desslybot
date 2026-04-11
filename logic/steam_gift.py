from logic.api.steam_gift_api import get_game_info_api, create_gift_order_api
from logic.repository.steam_gift_rep import create_steam_gift_order
from utils.exceptions import BotError, UserNotRegister, DontHaveFunds
import asyncio

async def searching_games(game_name, games_list):
    query = game_name.lower()
    filtered = [g for g in games_list if query in g.get('name').lower()][:15]
    return filtered

async def game_info_rendering(app_id):
    games = await get_game_info_api(app_id)
    processed_info = []
    for game in games:
        processed_info.append({'edition': game.get('edition'), 'package_id': game.get('package_id'), 'regions_info': game.get('regions_info', [])})
    return {'reg_info': processed_info}

async def steam_order_processing(uid, steam_link, region, package_id, price):
    if price is None:
        raise BotError('Произошла ошибка! Вернитесь в главное меню и выберите товар снова')
    api_res = await create_gift_order_api(steam_link=steam_link, region=region, package_id=package_id)
    order = await create_steam_gift_order(customer_id=uid, api_data=api_res, price=price)
    return(f'Заказ {order.transaction_id} успешно создан!')