import telepot
import sys
import time
from telepot.loop import MessageLoop


def sendNotification(message):
    f = open("subscribers.txt", "r")
    for line in f:
        bot.sendMessage(line, message)


bot = telepot.Bot('494856102:AAHCA__TrYFx6RjziauVINutEbdewrmHhDk')

if sys.argv[1] == "message" :
    sendNotification(sys.argv[2])
if sys.argv[1] == "time" :
    sendNotification(time.ctime())
