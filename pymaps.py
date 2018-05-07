import csv
import pyodbc
import googlemaps
from datetime import datetime

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

# Close connection
main_connection.close()

geocode_result = gmaps.geocode('Durham, NC')

print(str(geocode_result[0]['geometry']['location']['lat']) + ", " + str(geocode_result[0]['geometry']['location']['lng']))
