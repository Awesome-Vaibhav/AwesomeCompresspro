from telethon import TelegramClient
from decouple import config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = "7556932"
API_HASH = "6b99e012069f373abbcac581d3cdd6db"
BOT_TOKEN = "5504367878:AAHq7y5bO75Zym6MDbYb_46gQflhm6h6Pu8"
BOT_UN = "Awesome_Files_Compressor_Bot"

Drone = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 
