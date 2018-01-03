import time
import random
import datetime
import telepot
import os
import subprocess
import mmap
from telepot.loop import MessageLoop


def subscribe(chat_id):
    with open("subscribers.txt", "r+") as f:
        for line in f:
            if chat_id in line:
                bot.sendMessage(chat_id, "Already Subscribed!")
                break
        else:    
            f.write(str(chat_id + "\n"))
            bot.sendMessage(chat_id, "Subscription Successful!")


def unsubscribe(chat_id):
    f = open("subscribers.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i != chat_id + "\n":
            f.write(i)
    f.truncate()
    f.close()
    bot.sendMessage(chat_id, "Unsubscribed!")        
        

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
    elif command == '/subscribe':
        subscribe(str(chat_id))
    elif command == '/unsubscribe':
        unsubscribe(str(chat_id))
    else:
        bot.sendMessage(chat_id, "Oops! I don't seem to understand this command.")


bot = telepot.Bot('---key here---')

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)