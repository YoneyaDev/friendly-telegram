import time

from telethon.sync import TelegramClient
from telethon.tl import functions, types

API_ID = 8208885
API_HASH = "33fef87d80a6aac09f038b3fbfa85852"
TOKEN = 2103838470:AAEqhNCHvlIFPnlsLHRpzn2mOZgm4uBJY9s
CHAT_ID = "https://t.me/joinchat/wtscTw-_KHFmN2Vi"

client = TelegramClient("bot", API_ID, API_HASH)
client.start(bot_token=TOKEN)

while True:
 client.send_message(CHAT_ID, MESSAGE)
 time.sleep(60)

