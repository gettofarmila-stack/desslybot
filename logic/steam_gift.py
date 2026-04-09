


async def searching_games(game_name, games_list):
    query = game_name.lower()
    filtered = [g for g in games_list if query in g.get('name').lower()][:15]
    return filtered