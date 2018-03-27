from pycricbuzz import Cricbuzz
import json

c = Cricbuzz()
matches = c.matches()

for match in matches:
    print(match['srs'] + " - " + match['status'])


