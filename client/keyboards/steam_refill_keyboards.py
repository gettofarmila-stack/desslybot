from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def trade_select_currency_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='🇺🇸 USD', callback_data='currency_1'), types.InlineKeyboardButton(text='RUB 🇷🇺', callback_data='currency_5'))
    builder.row(types.InlineKeyboardButton(text='🇰🇿 KZT', callback_data='currency_37'), types.InlineKeyboardButton(text='UAH 🇺🇦', callback_data='currency_18'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def inline_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def confirm_buttons_login():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Подтвердить', callback_data=f'currency_choise', style='success'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def confirm_buttons(sum_in_usd, login):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm_refill_{sum_in_usd}_{login}', style='success'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()