import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config.env')
 
DEBUG_MODE = False   # изменить на True, чтобы включить режим тестирования (позволяет тестировать функции без апи, допустим у вас там нет денег)
REFERRAL_RATE = 0.005   # ставка по реферальной программе(процент отчислений за пополнения)
#просто данные
BOT_TOKEN = os.getenv('TOKEN')
DESSLY_TOKEN = os.getenv('DESSLY_TOKEN')
POSTGRES_URL = os.getenv('POSTGRES_URL')
MARKET_CHANNEL = os.getenv('MARKET_CHANNEL')
SUPPORT_LINK = os.getenv('SUPPORT_LINK')
REVIEW_LINK = os.getenv('REVIEW_LINK')
SERVICE_NAME = os.getenv('SERVICE_NAME')

#фотки, если хотите то тоже замените
MAIN_PHOTO = 'AgACAgQAAxkBAANvaddiaCdKNqlPQ37m_We4Xp0KFcsAAigNaxsY08BS6iU2QfZy8-gBAAMCAAN5AAM7BA'
LOGIN_PHOTO = 'AgACAgQAAxkBAAN2addi6pfwzOH6ZnzYfbn3u2DpAyQAAi0NaxsY08BSoTBGQp-lWecBAAMCAAN5AAM7BA'
ERROR_PHOTO = 'AgACAgQAAxkBAAN_addjzIXacE_FV4nBdRpdZ6X5Lt0AAjMNaxsY08BS1CuCA9Sf_n0BAAMCAAN5AAM7BA'
CONFIRM_PHOTO = 'AgACAgQAAxkBAAOCaddkQhii3z5YZhdV3ZWznEBw-bkAAjQNaxsY08BSEDVFPix5nLoBAAMCAAN5AAM7BA'
SUCCESS_PHOTO = 'AgACAgQAAxkBAAOhaddoby9kSE355-IVZKC2jWHpXcQAAjsNaxsY08BS2nJjILhw46wBAAMCAANtAAM7BA'
INVITE_LINK_PHOTO = 'AgACAgQAAxkBAAIBNmnZKRl2bcoRCjucRVytWzNret7mAALsDGsbCrjIUg-0N3RPjmgyAQADAgADbQADOwQ'