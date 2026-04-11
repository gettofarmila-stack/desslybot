from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from utils.get_cache import GAMES_CACHE


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
    builder.row(types.InlineKeyboardButton(text='Очистить поиск', callback_data='clear_search', style='danger'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def editions_builder(data: dict):
    builder = InlineKeyboardBuilder()
    for edition in data.get('reg_info', []):
        text = edition.get('edition')
        pkg_id = edition.get('package_id')
        builder.row(types.InlineKeyboardButton(text=text, callback_data=f"edition_{pkg_id}", style='primary'))
    builder.row(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='steam_gifts', style='danger'))
    builder.row(types.InlineKeyboardButton(text='🏠 Меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def regions_builder(reg_info: list, package_id: int):
    builder = InlineKeyboardBuilder()  
    for edition in reg_info:
        if edition.get('package_id') == package_id:
            for reg in edition.get('regions_info', []):
                btn_text = f"{reg['region']}: {reg['price']}$"
                callback = f"gift_{reg['region']}_{package_id}_{reg['price']}"
                builder.add(types.InlineKeyboardButton(text=btn_text, callback_data=callback, style='primary'))
    builder.adjust(2) 
    builder.row(types.InlineKeyboardButton(text='⬅️ Назад к изданиям', callback_data='back_to_editions', style='danger'))
    builder.row(types.InlineKeyboardButton(text='🏠 Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()