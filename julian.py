import os
import telepot
import time
import urllib3
import csv
from telepot.loop import MessageLoop

keys = {}
with open('keys.csv', newline='') as keystore:
    reader = csv.reader(keystore)
    next(reader)
    keys = dict(reader)

bot = telepot.Bot(keys['julian'])

scores = {"A": 1, "C": 3, "B": 3, "E": 1, "D": 2, "G": 2,
          "F": 4, "I": 1, "H": 4, "K": 5, "J": 8, "M": 3,
          "L": 1, "O": 1, "N": 1, "Q": 10, "P": 3, "S": 1,
          "R": 1, "U": 1, "T": 1, "W": 4, "V": 4, "Y": 4,
          "X": 8, "Z": 10}

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    response = []

    # Get the Scrabble rack from the user.
    if content_type == 'text':
        input_word = msg["text"]
        rack = input_word.upper()
    
    # Turn the words in the scrabblewords.txt file into a Python list.
    wordlist = []

    try:
        with open("scrabblewords.txt", "r") as f:
            for line in f:
                wordlist.append(line.strip())
    except EnvironmentError:
        print("Oops, I couldn't find scrabblewords.txt.")
        print("Please put the scrabblewords.txt and this file in the same folder and try again!")
        exit(1)

    # Find all of the valid words that can be made up of the letters in the rack.
    valid_words = []

    for word in wordlist:
        candidate = True
        rack_letters = list(rack)
        for letter in word:
            if letter not in rack_letters:
                candidate = False
                break # No need to keep checking letters.
            else:
                rack_letters.remove(letter)
        if candidate == True:
            # Get the Scrabble scores for each word.
            total = 0
            for letter in word:
                total = total + scores[letter]
            valid_words.append([total, word])
    
    # Print the valid words, sorted by Scrabble score.
    valid_words.sort()
    
    if not valid_words:
        response.append("No possible words found!")
    else:
        for entry in valid_words:
            score = entry[0]
            word = entry[1]
            response.append(str(score) + " " + word + "\n")

    bot.sendMessage(chat_id, ''.join(response))

MessageLoop(bot, handle).run_as_thread()

print('I am listening ...')

while 1:
    time.sleep(10)