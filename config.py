import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config.env')

BOT_TOKEN = os.getenv('TOKEN')
DESSLY_TOKEN = os.getenv('DESSLY_TOKEN')
POSTGRES_URL = os.getenv('POSTGRES_URL')