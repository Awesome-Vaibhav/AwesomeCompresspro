from telethon import TelegramClient
from decouple import config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = "7556932"
API_HASH = "6b99e012069f373abbcac581d3cdd6db"
BOT_TOKEN = config("BOT_TOKEN", default=None)
BOT_UN = config("BOT_UN", default=None)

Drone = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 
