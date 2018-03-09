import telepot
import sys
import time
import csv
from telepot.loop import MessageLoop


def sendNotification(message):
    f = open("subscribers.txt", "r")
    for line in f:
        bot.sendMessage(line, message)

keys = {}
with open('keys.csv', newline='') as keystore:
    reader = csv.reader(keystore)
    next(reader)
    keys = dict(reader)

bot = telepot.Bot(keys['jake'])

if sys.argv[1] == "message" :
    sendNotification(sys.argv[2])
if sys.argv[1] == "time" :
    sendNotification(time.ctime())
