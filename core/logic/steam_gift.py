from core.logic.api.steam_gift_api import get_game_info_api, create_gift_order_api
from core.logic.repository.steam_gift_rep import create_steam_gift_order
from core.logic.repository.user_rep import charge_balance, charge_balance_id
from utils.exceptions import BotError, UserNotRegister, DontHaveFunds


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
    await charge_balance_id(amount=price, user=uid)
    api_res = await create_gift_order_api(steam_link=steam_link, region=region, package_id=package_id)
    order = await create_steam_gift_order(customer_id=uid, api_data=api_res, price=price)
    return(f'Заказ {order.transaction_id} успешно создан!')

async def steam_gift_processing_fastapi(user, steam_link, region, package_id, app_id):
    game_packages = await get_game_info_api(app_id)
    current_package = next((package for package in game_packages if package['package_id'] == package_id), None)
    if not current_package:
        raise BotError('Invalid package_id')
    regions_list = current_package.get('regions_info', [])
    region_data = next((reg for reg in regions_list if reg['region'] == region), None)
    if not region_data:
        raise BotError('Invalid region')
    price = float(region_data['price'])
    await charge_balance_id(amount=price, user=user.user_id)
    api_res = await create_gift_order_api(steam_link=steam_link, region=region, package_id=package_id)
    order = await create_steam_gift_order(customer_id=user.user_id, api_data=api_res, price=price)
    return {
        'transaction_id': order.transaction_id,
        'status': order.status
            }