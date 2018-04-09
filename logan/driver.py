import os
import py2neo
import json
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs

# Connect to neo4j
neo4jUrl = "http://localhost:7474/db/data"
graph = py2neo.Graph(neo4jUrl, password='password')
print "neo4j connected"

files = ['/index.html']
scripts = ['/querying/script.js']
queries = {
  '/categories': 'querying/categories.cql',
  '/overlap': 'querying/overlap.cql'
  }

class Neo4jRequest(BaseHTTPRequestHandler):
  def do_GET(self):
    url = urlparse(self.path)
    path = url.path
    params = parse_qs(url.query)
    if path in files or path in scripts:
      print "serving file"
      self.send_response(200)
      self.send_header('Content-type', 'text/html' if path in files else 'text/javascript')
      self.end_headers()
      with open(path[1:]) as html:
        text = html.read()
        self.wfile.write(text)
      self.wfile.close()
    elif path in queries.keys():
      print "connecting neo4j"
      with open(queries[path]) as f:
        query = f.read()
      print(params)
      result = graph.run(query, params)
      self.send_response(200)
      self.send_header('Content-type', 'text/json')
      self.end_headers()
      self.wfile.write(json.dumps(result.data()))
      self.wfile.close()

print "handler defined"

httpd = SocketServer.TCPServer(('', 8080), Neo4jRequest)
print "server initiated"
httpd.serve_forever()
