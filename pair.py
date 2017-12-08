import random

candidates = ['Candidate A', 'Candidate B', 'Candidate C', 'Candidate D', 'Candidate E', 'Candidate F', 'Candidate G', 'Candidate H']

random.shuffle(candidates)

for i in range(len(candidates)):
    print(candidates[i] + " buys for " + candidates[(i+1)%(len(candidates))])