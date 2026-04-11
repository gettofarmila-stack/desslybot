from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder



def voucher_builder(vouchers, page: int=0):
    builder = InlineKeyboardBuilder()
    page_size = 5
    start_idx = page * page_size
    end_idx = start_idx + page_size
    current_vouchers = vouchers[start_idx:end_idx]
    builder.row(types.InlineKeyboardButton(text='🔍 Поиск по названию', callback_data='search_voucher', style='success'))
    for voucher_name, voucher_id in current_vouchers:
        builder.row(types.InlineKeyboardButton(text=voucher_name, callback_data=f'select_voucher_{voucher_id}', style='primary'))
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'vouchers_page_{page - 1}', style='danger'))
    if end_idx < len(vouchers):
        nav_buttons.append(types.InlineKeyboardButton(text='Вперед ➡️', callback_data=f'vouchers_page_{page + 1}', style='danger'))
    if nav_buttons:
        builder.row(*nav_buttons)
    builder.row(types.InlineKeyboardButton(text='Очистить поиск', callback_data='clear_voucher_search', style='danger'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def variations_builder(variations):
    builder = InlineKeyboardBuilder()
    for var in variations:
        builder.row(types.InlineKeyboardButton(text=var['name'], callback_data=f'variation_{var['id']}', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Назад', callback_data='vouchers', style='danger'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def confirm_variation_builder(voucher_id, var_id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Подтвердить', callback_data=f'buy_voucher_{voucher_id}_{var_id}', style='success'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()