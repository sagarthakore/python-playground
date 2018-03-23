import time
import random
import datetime
import telepot
import os
import subprocess
import csv
import mmap
import urllib3
from telepot.loop import MessageLoop
from requests import get

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
        

def sendNotification(message):
    f = open("subscribers.txt", "r")
    for line in f:
        bot.sendMessage(line, message)


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/start':
        bot.sendMessage(chat_id, "Hi! I'm Jake! I am a half baked AI bot running on Sagar's Work Machine ready to perform some tasks for you. Pick a command from the list and I will try my best!" + "\n1. /roll - Toll a six sided die.\n2. /time - Show the current system time.\n3. /about - Information about the bot.\n4. /crypto - Get current crypto currency exchange rates.")
    elif command == '/roll':
        bot.sendMessage(chat_id, str(random.randint(1,6)) + "  That was quick wasn't it?")
    elif command == '/time':
        bot.sendMessage(chat_id, "The time is " + str(time.strftime("%I:%M %p")))
    elif command == '/about':
        bot.sendMessage(chat_id, "Hi I'm Jake! I am a half baked AI bot created by Sagar. He is still training me to be more useful. Currently I am running on his Work Machine.")
    elif command == '/subscribe':
        subscribe(str(chat_id))
    elif command == '/unsubscribe':
        unsubscribe(str(chat_id))
    elif command == '/crypto':
        url = 'https://api.coinbase.com/v2/prices/USD/spot?'
        response = get(url).json()
        bot.sendMessage(chat_id, "BTC: $"+response['data'][0]['amount'] + "\n" + "BCH: $"+response['data'][1]['amount'] + "\n" + "ETH: $"+response['data'][2]['amount'] + "\n" + "LTC: $"+response['data'][3]['amount'])
    else:
        bot.sendMessage(chat_id, "Oops! I don't seem to understand this command. These are the only commands I can understand: " + "\n1. /roll - Toll a six sided die.\n2. /time - Show the current system time.\n3. /about - Information about the me.\n4. /crypto - Get current crypto currency exchange rates.")


keys = {}
with open('keys.csv', newline='') as keystore:
    reader = csv.reader(keystore)
    next(reader)
    keys = dict(reader)

bot = telepot.Bot(keys['jake'])

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)