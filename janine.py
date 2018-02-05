import telepot
import sys
import time
from telepot.loop import MessageLoop
from bs4 import BeautifulSoup
from requests import get


def sendNotification(message):
    f = open("subscribers.txt", "r")
    for line in f:
        bot.sendMessage(line, message)


bot = telepot.Bot('494856102:AAHCA__TrYFx6RjziauVINutEbdewrmHhDk')

url = 'https://api.coinbase.com/v2/prices/USD/spot?'
response = get(url).json()

sendNotification("$"+response['data'][0]['amount'])