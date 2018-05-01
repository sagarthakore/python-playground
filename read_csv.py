import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

policy_id = []
county_name = []
counties = []
count = []
construction = []
myData = []

with open('sample.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvDataFile)
    for row in csvReader:
        policy_id.append(row[0])
        county_name.append(row[2])
        construction.append(row[16])
        myData.append(row)


myData = Counter(county_name)
plt.bar(range(len(myData)), list(myData.values()), align='center')
plt.xticks(range(len(myData)), list(myData.keys()))
plt.show()

# myData = Counter(construction)
# # plt.xticks(rotation=30)
# plt.bar(range(len(myData)), list(myData.values()), align='center')
# plt.xticks(range(len(myData)), list(myData.keys()))
# plt.show()



# plt.plot(Counter(county_name))
# plt.show()

# Counter(county_name)
# print(Counter(county_name))
# print(county_name.count(county_name))

# unique_county_name = sorted(list(set(county_name)))
# print(unique_county_name[47])