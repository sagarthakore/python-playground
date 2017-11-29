import random

candidates = ['Ganshyam Dada', 'Anila Ba', 'Usha Ba', 'Rupa Mami', 'Krupa Maasi', 'Kaushal Mama', 'Mom', 'Amisha Maasi']

random.shuffle(candidates)

for i in range(len(candidates)):
    print(candidates[i] + " buys for " + candidates[(i+1)%(len(candidates))])