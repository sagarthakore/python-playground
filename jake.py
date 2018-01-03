import time
import random
import datetime
import telepot
import os
import subprocess
from telepot.loop import MessageLoop

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/about':
        bot.sendMessage(chat_id, 'Bot created by Sagar. Running on Work Machine.')
    else:
        bot.sendMessage(chat_id, "Oops! I don't seem to understand this command.")

bot = telepot.Bot('----key here----')

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)