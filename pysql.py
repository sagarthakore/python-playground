import csv
import pyodbc

# Get connection string
keys = {}
with open('connection.csv', newline='') as keystore:
    reader = csv.reader(keystore)
    next(reader)
    keys = dict(reader)
connection_string = keys['pydb']

# Establish connection to the database
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# Execute SQL command
SQLCommand = ("select * from sampledata where policyID = '119736'")
cursor.execute(SQLCommand)
results = cursor.fetchone() 

# Print the results
while results:
    print("Policy Id: " + str(results.policyID))
    print("State Code: " + str(results.statecode))
    print("County: " + str(results.county))
    print("Latitude: " + str(results.point_latitude))
    print("Longitude: " + str(results.point_longitude))
    results = cursor.fetchone()

# Close the connection
connection.close()