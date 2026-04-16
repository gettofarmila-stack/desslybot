from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import REFERRAL_RATE, DOCS_LINK


def profile_builder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='История заказов', callback_data='order_history', style='primary'), types.InlineKeyboardButton(text='Пополнение', callback_data='topup', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Реферальная Программа', callback_data='referral_system', style='primary'), types.InlineKeyboardButton(text='Наш API', callback_data='developer_panel', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def order_history_builder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Ваучеры', callback_data='voucher_order_history', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Назад', callback_data='profile', style='danger'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def referral_system_builder(user_referrals):
    global REFERRAL_RATE
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f'Ставка:\n{REFERRAL_RATE * 100}%', callback_data='none'), types.InlineKeyboardButton(text=f'Приглашено:\n{user_referrals} чел.', callback_data='none'))
    builder.row(types.InlineKeyboardButton(text='Назад', callback_data='profile', style='danger'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def developer_menu_builder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Документация', url=DOCS_LINK, callback_data='none', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Перевыпустить ключ', callback_data='api_key_reload', style='success'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()