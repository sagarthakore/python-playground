from bs4 import BeautifulSoup
from requests import get

raleigh_weather = 'http://forecast.weather.gov/MapClick.php?lat=35.8063&lon=-78.7804#.WlezT6inGM8'

page = get(raleigh_weather)
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

detail_forecast = soup.find(id="detailed-forecast-body")
forecast_label = detail_forecast.find(class_="forecast-label").get_text()
forecast_text = detail_forecast.find(class_="forecast-text").get_text()


# print(forecast_label)
# print(forecast_text)
# print(temp)

print(forecast_label + "\n" + forecast_text + "\n" + temp)
