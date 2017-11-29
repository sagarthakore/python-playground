"""Jumbled word solver"""

import os

def readfile():
    """Read the file that contains all the dictionary words and return them as an array"""
    words = []
    try:
        with open("words_en.txt", "r") as file:
            for line in file:
                words.append(line.strip())
    except EnvironmentError:
        print("Shoot! Could not find words_en.txt")
        print("Make sure this words_en.txt and this file is in the same folder and try again!")
        exit(1)
    return words


def getkey(inputword):
    """Return the hash key for the word"""
    return ''.join(sorted(inputword))


def clear_output():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

# Start
WORDSARRAY = readfile()
HASHWORDS = {}
for word in WORDSARRAY:
    arrwords = []
    arrwords.append(word)
    if getkey(word) in HASHWORDS:
        arrwords = HASHWORDS[getkey(word)]
        arrwords.append(word)
    HASHWORDS[getkey(word)] = arrwords

while True:
    clear_output()
    TESTWORD = input("Enter a jumbled word: ")
    if getkey(TESTWORD) in HASHWORDS:
        print("Dictionary words are: ")
        for word in HASHWORDS[getkey(TESTWORD)]:
            print(word)
    else:
        print("No dictionary words found!")

    REPLAY = input("Continue? y/n ")
    if REPLAY[0].lower() != 'y':
        clear_output()
        break
# End
