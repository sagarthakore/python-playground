import time
import random
import datetime
import telepot
import os
import subprocess
import mmap
from telepot.loop import MessageLoop
from requests import get

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/rates':
        url = 'https://api.coinbase.com/v2/prices/USD/spot?'
        response = get(url).json()
        bot.sendMessage(chat_id, "BTC: $"+response['data'][0]['amount'] + "\n" + "BCH: $"+response['data'][1]['amount'] + "\n" + "ETH: $"+response['data'][2]['amount'] + "\n" + "LTC: $"+response['data'][3]['amount'])
    else:
        bot.sendMessage(chat_id, "Oops! I don't seem to understand this command. Text '/rates' to see the current exchange rates.")


bot = telepot.Bot('450826388:AAExq8IUAauw2BuZTyIRjy3dP2ibB5hgXZc')

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)