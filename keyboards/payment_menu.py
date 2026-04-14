from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def payment_builder(url, payment_id):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Оплатить', url=url, callback_data='none', style='success'))
    builder.row(types.InlineKeyboardButton(text='Я уже оплатил', callback_data=f'payment_update_{payment_id}', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu', style='danger'))
    return builder.as_markup()