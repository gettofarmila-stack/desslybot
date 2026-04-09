from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from utils.gift_games_list import GAMES_CACHE


def games_builder(all_games: list=GAMES_CACHE, page: int=0):
    builder = InlineKeyboardBuilder()
    page_size = 5
    start_idx = page * page_size
    end_idx = start_idx + page_size
    current_games = all_games[start_idx:end_idx]
    builder.row(types.InlineKeyboardButton(text='🔍 Поиск по названию', callback_data='search_by_name', style='success'))
    for game in current_games:
        builder.row(types.InlineKeyboardButton(text=game['name'], callback_data=f'buy_game_{game['appid']}', style='primary'))
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'games_page_{page - 1}', style='danger'))
    if end_idx < len(all_games):
        nav_buttons.append(types.InlineKeyboardButton(text='Вперед ➡️', callback_data=f'games_page_{page + 1}', style='danger'))
    if nav_buttons:
        builder.row(*nav_buttons)
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()