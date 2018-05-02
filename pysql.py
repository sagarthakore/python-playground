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
    print("Policy Id: " + str(results[0]))
    print("State Code: " + str(results[1]))
    print("County: " + str(results[2]))
    print("Latitude: " + str(results[3]))
    print("Longitude: " + str(results[4]))
    results = cursor.fetchone()

# Close the connection
connection.close()