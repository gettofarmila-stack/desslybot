from logic.api.steam_gift_api import get_game_info_api
import asyncio

async def searching_games(game_name, games_list):
    query = game_name.lower()
    filtered = [g for g in games_list if query in g.get('name').lower()][:15]
    return filtered

async def game_info_rendering(app_id):
    games = await get_game_info_api(app_id)
    if games is False or not games:
        return False
    processed_info = []
    for game in games:
        processed_info.append({'edition': game.get('edition'), 'package_id': game.get('package_id'), 'regions_info': game.get('regions_info', [])})
    return {'reg_info': processed_info}