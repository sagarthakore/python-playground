import csv

myData = [["First Name", "Last Name", "Position"], ['Sagar', 'Thakore', 'Developer'], ['Steve','Jobs','CEO']]  
myFile = open('testfile.csv', 'w', newline='')  
with myFile:  
   writer = csv.writer(myFile)
   writer.writerows(myData)