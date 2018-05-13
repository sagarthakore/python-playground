import telepot
import sys
import time
import csv
import urllib3
import pyodbc
from telepot.loop import MessageLoop

# Get connection string
keys = {}
with open('connection.csv', newline='') as keystore:
    reader = csv.reader(keystore)
    next(reader)
    keys = dict(reader)
connection_string = keys['pydb']

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

# Establish connection to the database
main_connection = pyodbc.connect(connection_string)
main_cursor = main_connection.cursor()

# Execute SQL command
SQLCommand = ("select * from conf_keys where application = 'janet'")
main_cursor.execute(SQLCommand)
results = main_cursor.fetchone() 

# Close the connection
main_connection.close()

# Apply the key to bot
bot = telepot.Bot(str(results.key))

if sys.argv[1] == "message" :
    sendNotification(sys.argv[2])
if sys.argv[1] == "time" :
    sendNotification(time.ctime())
