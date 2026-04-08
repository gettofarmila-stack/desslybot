import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config.env')

BOT_TOKEN = os.getenv('TOKEN')
DESSLY_TOKEN = os.getenv('DESSLY_TOKEN')
POSTGRES_URL = os.getenv('POSTGRES_URL')
MARKET_CHANNEL = os.getenv('MARKET_CHANNEL')
SUPPORT_LINK = os.getenv('SUPPORT_LINK')
REVIEW_LINK = os.getenv('REVIEW_LINK')
SERVICE_NAME = os.getenv('SERVICE_NAME')