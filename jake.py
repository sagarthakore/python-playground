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
import pytz

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
SQLCommand = ("select * from conf_keys where application = 'jake'")
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

def sendNotificationToSubscriber(chatid, message):
    io_connection = pyodbc.connect(connection_string)
    io_cursor = io_connection.cursor()
    subscriber = ("select * from subscribers where [status] = 1 and subscriber_id = ?")
    param = chatid
    io_cursor.execute(subscriber, param)
    results = io_cursor.fetchone()
    while(results):
        bot.sendMessage(str(results.subscriber_id), message)
        results = io_cursor.fetchone()
    io_connection.close()

def sendReminders():
    io_connection = pyodbc.connect(connection_string)
    io_cursor = io_connection.cursor()
    reminders = ("select * from reminders where [status] = 1")
    io_cursor.execute(reminders)
    results = io_cursor.fetchone()
    while(results):
        if(results.daily == 1):
            if(results.time.strftime("%H:%M") == time.strftime("%H:%M")):
                sendNotificationToSubscriber(results.subscriber_id, results.message)
        else:
            if(results.time.strftime("%H:%M") == time.strftime("%H:%M") and results.day == datetime.datetime.today().weekday()):
                sendNotificationToSubscriber(results.subscriber_id, results.message)
        results = io_cursor.fetchone()
    io_connection.close()

def convertToUTC24(input_time):

    curr_date = datetime.datetime.now().date()
    time_string = str(curr_date) + " " + input_time
    local = pytz.timezone ("US/Eastern")
    # naive = datetime.datetime.strptime("2001-2-3 10:11:12", "%Y-%m-%d %H:%M:%S")
    naive = datetime.datetime.strptime(time_string, '%Y-%m-%d %I:%M%p')
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc).strftime('%H:%M')
    return str(utc_dt)

def setReminder(chat_id, name, daily, day, time, message):
    io_connection = pyodbc.connect(connection_string)
    io_cursor = io_connection.cursor()
    check_command = ("select * from reminders where subscriber_id = ? and name = ? and [status] = 1")
    param_chat_id = chat_id
    io_cursor.execute(check_command, name, param_chat_id)
    results = io_cursor.fetchone()
    if(results != None):
        bot.sendMessage(chat_id, "A reminder with that name already exists. Please choose a different name!") 
    else:
        set_reminder = ("insert into reminders (subscriber_id, name, daily, day, time, message, status, create_datetime) values (?,?,?,?,?,?,?,?)")
        values = [str(chat_id), str(name), int(daily), int(day), time, message, 1, datetime.datetime.now()]
        io_cursor.execute(set_reminder, values)
        io_connection.commit()
        bot.sendMessage(chat_id, "Reminder Set!")
    io_connection.close()

def showAllReminders(chat_id):
    io_connection = pyodbc.connect(connection_string)
    io_cursor = io_connection.cursor()
    show_reminders = ("select * from reminders where [status] = 1 and subscriber_id = ?")
    values = [str(chat_id)]
    io_cursor.execute(show_reminders, values)
    results = io_cursor.fetchone()
    reminderlist = []
    while(results):
        reminderlist.append(results.name)
        results = io_cursor.fetchone()
    for remindername in reminderlist:
        bot.sendMessage(chat_id, remindername + "\n")
    io_connection.close()

def deleteReminder(chat_id, name):
    io_connection = pyodbc.connect(connection_string)
    io_cursor = io_connection.cursor()
    check_reminder = ("select * from reminders where subscriber_id = ? and [status] = 1")
    param_chat_id = chat_id
    io_cursor.execute(check_reminder, param_chat_id)
    results = io_cursor.fetchone()
    if(results != None):
        bot.sendMessage(chat_id, "No reminder set with that name!") 
    else:
        delete_reminder = ("update reminders set [status] = 0 , lastupdate_datetime = ? where subscriber_id = ? and name = ?")
        values = [datetime.datetime.now(), str(chat_id), str(name)]
        io_cursor.execute(delete_reminder, values)
        io_connection.commit()
        bot.sendMessage(chat_id, "Reminder Deleted!")
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
    elif command == '/setreminder':
        bot.sendMessage(chat_id, data['reminder_input'])
    elif command[:7].lower() == "address":
        try:
            geocode_result = gmaps.geocode(msg['text'][1:])
            bot.sendMessage(chat_id, "Formatted Address: \n" + str(geocode_result[0]['formatted_address']))
        except:
            bot.sendMessage(chat_id, data['address_error'])
    elif command[:8].lower() == "reminder":
        try:
            reminder = []
            reminder = str(msg['text']).split(",")
            reminder_time = convertToUTC24(reminder[4])
            setReminder(chat_id, reminder[1], reminder[2], reminder[3], reminder_time, reminder[5])
        except:
            bot.sendMessage(chat_id, data['reminder_error'])
    else:
        bot.sendMessage(chat_id, str(data['error']).replace("\\n", "\n"))


MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')


while 1:
    time.sleep(60)
    sendReminders()