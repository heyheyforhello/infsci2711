import os
import requests
import py2neo
import json

# NOTES
# script located in project folder
# JSON data located in /data/dataset/
# Run python SimpleHTTPServer in project directory
# In Neo4j, created new project named "2711 Project"
# Inside that project created new database "yelpData" with password 'password'

# Connect to neo4j
neo4jUrl = "http://localhost:7474/db/data"
graph = py2neo.Graph(neo4jUrl, password='password')
print "neo4j connected"

# This is what counts as defining a schema
#graph.schema.create_uniqueness_constraint('Business', 'business_id')
#graph.schema.create_uniqueness_constraint('Category', 'name')
#graph.schema.create_uniqueness_constraint('User', 'user_id')
#print "constraints added"

# Load data in chunks of 10000
for dataType in ['user']:
  print 'loading ' + dataType
  with open ('load_' + dataType + '.cql') as queryFile:
    query = queryFile.read()
  with open('data/dataset/' + dataType + '.json') as dataFile:
    counter = 0
    acc = []
    for b in dataFile:
      counter += 1
      acc.append(json.loads(b))
      if counter == 10000:
        result = graph.run(query, json={'data': acc})
        print 'database update ' + dataType + ':' + str(result.next()['count'])
        acc = []
        counter = 0
    result = graph.run(query, json={'data': acc})
    print 'database update ' + dataType + ':' + str(result.next()['count'])
  print 'finished ' + dataType

