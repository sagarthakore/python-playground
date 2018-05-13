import time
import random
import telepot
import os
import subprocess
import csv
import mmap
import urllib3
import pyodbc
import datetime
import googlemaps
from telepot.loop import MessageLoop
from requests import get

# Get connection string
keys = {}
with open('connection.csv', newline='') as keystore:
    reader = csv.reader(keystore)
    next(reader)
    keys = dict(reader)
connection_string = keys['pydb']

# Establish connection to the database
main_connection = pyodbc.connect(connection_string)
main_cursor = main_connection.cursor()

# Execute SQL command
SQLCommand = ("select * from conf_keys where application = 'gmaps'")
main_cursor.execute(SQLCommand)
results = main_cursor.fetchone() 

# Apply the key to gmaps
gmaps = googlemaps.Client(key=str(results.key))

# Execute SQL command
SQLCommand = ("select * from conf_keys where application = 'jake_dev'")
main_cursor.execute(SQLCommand)
results = main_cursor.fetchone() 

# Apply the key to bot
bot = telepot.Bot(str(results.key))

# Execute SQL command
SQLCommand = ("select * from conf_data")
main_cursor.execute(SQLCommand)
results = main_cursor.fetchone() 

# Store results in a dictionary
data = {}
while results:
    data[str(results.key)] = str(results.value)
    results = main_cursor.fetchone()



def subscribe(chat_id):
    io_connection = pyodbc.connect(connection_string)
    io_cursor = io_connection.cursor()
    check_command = ("select * from subscribers where subscriber_id = ? and [status] = 1")
    param_chat_id = chat_id
    io_cursor.execute(check_command, param_chat_id)
    results = io_cursor.fetchone()
    if(results != None):
        bot.sendMessage(chat_id, "Already Subscribed!") 
    else:
        subscribe_command = ("insert into subscribers (subscriber_id, status, create_datetime) values (?,?,?)")
        values = [str(chat_id), 1, datetime.datetime.now()]
        io_cursor.execute(subscribe_command, values)
        io_connection.commit()
        bot.sendMessage(chat_id, "Subscription Successful!")
    io_connection.close() 


def unsubscribe(chat_id):
    io_connection = pyodbc.connect(connection_string)
    io_cursor = io_connection.cursor()
    check_command = ("select * from subscribers where subscriber_id = ? and [status] = 1")
    param_chat_id = chat_id
    io_cursor.execute(check_command, param_chat_id)
    results = io_cursor.fetchone()
    if(results == None):
        bot.sendMessage(chat_id, "Not Subscribed!") 
    else:
        subscribe_command = ("update subscribers set [status] = 0 , lastupdate_datetime = ? where subscriber_id = ?")
        values = [datetime.datetime.now(), chat_id]
        io_cursor.execute(subscribe_command, values)
        io_connection.commit()
        bot.sendMessage(chat_id, "Unsubscribed!") 
    io_connection.close()

def sendNotification(message):
    io_connection = pyodbc.connect(connection_string)
    io_cursor = io_connection.cursor()
    all_subscribers = ("select * from subscribers where [status] = 1")
    io_cursor.execute(all_subscribers)
    results = io_cursor.fetchone()
    while(results):
        bot.sendMessage(str(results.subscriber_id), message)
        results = io_cursor.fetchone()
    io_connection.close()

# Close the connection
main_connection.close()

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)

    if command == '/start':
        bot.sendMessage(chat_id, str(data['start']).replace("\\n", "\n"))
    elif command == '/roll':
        bot.sendMessage(chat_id, str(random.randint(1,6)) + " " + data['roll'])
    elif command == '/time':
        bot.sendMessage(chat_id, data['time'] + " " + str(time.strftime("%I:%M %p")))
    elif command == '/about':
        bot.sendMessage(chat_id, data['about'])
    elif command == '/subscribe':
        subscribe(str(chat_id))
    elif command == '/unsubscribe':
        unsubscribe(str(chat_id))
    elif command == '/crypto':
        url = data['crypto_url']
        response = get(url).json()
        bot.sendMessage(chat_id, "BTC: $"+response['data'][0]['amount'] + "\n" + "BCH: $"+response['data'][1]['amount'] + "\n" + "ETH: $"+response['data'][2]['amount'] + "\n" + "LTC: $"+response['data'][3]['amount'])
    elif command == '/formataddress':
        bot.sendMessage(chat_id, data['address_input'])
    elif command[:7].lower() == "address":
        try:
            geocode_result = gmaps.geocode(msg['text'][1:])
            bot.sendMessage(chat_id, "Formatted Address: \n" + str(geocode_result[0]['formatted_address']))
        except:
            bot.sendMessage(chat_id, data['address_error'])
    else:
        bot.sendMessage(chat_id, str(data['error']).replace("\\n", "\n"))


MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')


while 1:
    time.sleep(10)