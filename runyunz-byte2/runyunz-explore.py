import httplib2
from apiclient.discovery import build
import urllib
import json
import csv
import matplotlib.pyplot as plt 
import numpy as np

# This API key is provided by google as described in the tutorial
API_KEY = 'AIzaSyBC3xSAbpqAIdYC_OrZP_FtwfkF_XbkR0Q'

# This is the table id for the fusion table
TABLE_ID = '1l8GVeoIMH5ggV-UF3khJ5SDMT7RN4H9wwzRLsr4'

# open the data stored in a file called "data.json"
try:
    fp = open("data.json")
    response = json.load(fp)
# but if that file does not exist, download the data from fusiontables
except IOError:
    service = build('fusiontables', 'v1', developerKey=API_KEY)
    query = "SELECT * FROM " + TABLE_ID + " WHERE  AnimalType IN ('DOG','CAT')"
    response = service.query().sql(sql=query).execute()
    fp = open("data.json", "w+")
    json.dump(response, fp)


# this will be our summary of the data. For each column name, it will store
# a dictionary containing the number of occurences of each possible
# value for that column in the data. For example, for gender, 
# the possible values are "MALE" and "FEMALE" and "UNKNOWN"
# summary will contain {"MALE": 5199, "FEMALE": 4354, "UNKNOWN":82} 
# indicating that in the data, 5199 rows are marked as MALE, 
# 4354 rows are marked as FEMALE and 82 rows are marked as UNKNOWN
summary = {} 
columns = response['columns'] # the names of all columns
rows = response['rows'] # the actual data 

# how many rows are in the data we downloaded?
# this should be the same as in the fusion table
print len(rows)
# print rows[1]

# print columns
consider = [u'AnimalType', u'OutcomeType']
dog = {}
cat = {}

for row in rows:
	value = row[0]
	if type(value) is unicode:
		value = value.encode('ascii','ignore')
	if value == '':
		value = 'EMPTY'
	if value == 'NaN':
		value = 'EMPTY'

	if row[2] == u'DOG':
		try:
			dog[value] += 1
		except KeyError:
			dog[value] = 1
	elif row[2] == u'CAT':
		try:
			cat[value] += 1
		except KeyError:
			cat[value] = 1

for k in cat:
	if k not in dog:
		dog[k]=0
for k in dog:
	if k not in cat:
		dog[k]=0

print dog
print cat

N = max(len(dog), len(cat))
print N
ind = np.arange(N)
width = 0.6


pDog = plt.bar(ind, dog.values(), width, color='r', align='center')
pCat = plt.bar(ind, cat.values(), width, bottom=dog.values(), color='y', align='center')

plt.ylabel('Counts')
plt.title('Counts by Outcome Type and Animal Type')
plt.xticks(ind, dog.keys(), fontsize=10, rotation=90)
plt.legend((pDog[0], pCat[0]), ('Dog', 'Cat'))

plt.show()

countDog = 0
countCat = 0
for d in dog:
	countDog += dog[d]
for c in cat:
	countCat += cat[c]

pDog = plt.bar(0, countDog, 0.3, color='r', align='center')
pCat = plt.bar(1, countCat, 0.3, color='y', align='center')
plt.ylabel('Counts')
plt.title('Dog Counts vs Cat Counts')
plt.xticks((0,1), ("Dog","Cat"))

plt.show()

