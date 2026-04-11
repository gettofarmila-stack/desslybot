from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import REVIEW_LINK, SUPPORT_LINK, MARKET_CHANNEL

def main_menu_builder():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text='Пополнение Steam', callback_data='steam_refill', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Steam Gifts', callback_data='steam_gifts', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Ваучеры', callback_data='vouchers', style='primary'))
    builder.row(types.InlineKeyboardButton(text='Наш Telegram', url=MARKET_CHANNEL, style='danger'), types.InlineKeyboardButton(text='Тех. Поддержка', url=SUPPORT_LINK, style='danger'))
    builder.row(types.InlineKeyboardButton(text='Отзывы', url=REVIEW_LINK))
    builder.row(types.InlineKeyboardButton(text='Личный кабинет', callback_data='profile', style='success'))
    return builder.as_markup()