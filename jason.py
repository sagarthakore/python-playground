from bs4 import BeautifulSoup
from requests import get

url = 'https://api.coinbase.com/v2/prices/USD/spot?'
response = get(url).json()
print(response)
print("BTC: $"+response['data'][0]['amount'] + "\n" + "BCH: $"+response['data'][1]['amount'] + "\n" + "ETH: $"+response['data'][2]['amount'] + "\n" + "LTC: $"+response['data'][3]['amount'])
