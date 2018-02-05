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

source = 'https://junction.niehs.nih.gov/'

page = get(source)
soup = BeautifulSoup(page.content, 'html.parser')

block = soup.find(id = "jh-word-of-the-day")
word = block.find(id = "jh-word-of-the-day-word").get_text()
definition = block.find(id = "jh-word-of-the-day-definition").get_text()

sendNotification("Word of the day" + "\n\n" + word.strip() + "\n\n" + definition.strip() + "\n")