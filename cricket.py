from pycricbuzz import Cricbuzz
import json

c = Cricbuzz()
matches = c.matches()


for match in matches:
    if (match['mchstate'] == 'Result'):
        data = c.livescore(match['id'])
        print(data['matchinfo']['srs'] + " - " + data['matchinfo']['status'])
        print(data['batting']['team'] + " - " + data['batting']['score'][0]['runs'] + "/" + data['batting']['score'][0]['wickets'] + " - " + data['batting']['score'][0]['overs'] + " over(s)")
        print(data['bowling']['team'] + " - " + data['bowling']['score'][0]['runs'] + "/" + data['bowling']['score'][0]['wickets'] + " - " + data['bowling']['score'][0]['overs'] + " over(s)")
    if(match['mchstate'] == 'nextlive'):
        print(match['srs'] + " - " + match['status'])
