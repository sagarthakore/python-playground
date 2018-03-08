import os
import telepot
import time
import urllib3
import csv
from telepot.loop import MessageLoop

# You can leave this bit out if you're using a paid PythonAnywhere account
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# end of the stuff that's only needed for free accounts

def sendNotification(message):
    f = open("subscribers.txt", "r")
    for line in f:
        bot.sendMessage(line, message)

keys = {}
with open('keys.csv', newline='') as keystore:
    reader = csv.reader(keystore)
    next(reader)
    keys = dict(reader)

bot = telepot.Bot(keys['jaden'])

def readfile():
    """Read the file that contains all the dictionary words and return them as an array"""
    words = []
    try:
        with open("words_en.txt", "r") as file:
            for line in file:
                words.append(line.strip())
    except EnvironmentError:
        exit(1)
    return words


def getkey(inputword):
    """Return the hash key for the word"""
    return ''.join(sorted(inputword))


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    response = []

    
    if content_type == 'text':
        input_word = msg["text"]
        TESTWORD = input_word.lower()
        WORDSARRAY = readfile()
        HASHWORDS = {}
        for word in WORDSARRAY:
            arrwords = []
            arrwords.append(word)
            if getkey(word) in HASHWORDS:
                arrwords = HASHWORDS[getkey(word)]
                arrwords.append(word)
            HASHWORDS[getkey(word)] = arrwords

        if getkey(TESTWORD) in HASHWORDS:
            response.append("Dictionary words are: \n\n")
            for word in HASHWORDS[getkey(TESTWORD)]:
                response.append(word + "\n")
        else:
            response.append("No dictionary words found!")
    
    bot.sendMessage(chat_id, ''.join(response))


MessageLoop(bot, handle).run_as_thread()

WORDSARRAY = readfile()
HASHWORDS = {}
for word in WORDSARRAY:
    arrwords = []
    arrwords.append(word)
    if getkey(word) in HASHWORDS:
        arrwords = HASHWORDS[getkey(word)]
        arrwords.append(word)
    HASHWORDS[getkey(word)] = arrwords

print('I am listening ...')

while 1:
    time.sleep(10)