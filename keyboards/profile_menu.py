from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import REFERRAL_RATE


def profile_builder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='История заказов', callback_data='order_history', style='primary'), types.InlineKeyboardButton(text='Пополнение', callback_data='topup', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Реферальная Программа', callback_data='referral_system', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()

def order_history_builder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Steam', callback_data='steam_order_history', style='primary'), types.InlineKeyboardButton(text='Ваучеры', callback_data='voucher_order_history', style='primary'))
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

