import py2neo
import json

def openRatioByRegion():
  """returns JSON with columns open_ratio and name, rows are neighborhoods"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business)-[:LOCATED_IN]-> (c:Neighborhood)
  with count(a) as total, c
  match (a:Business {is_open: 1}) -[:LOCATED_IN]-> (c:Neighborhood)
  return (count(a)*1.0/total) as open_ratio, c.name as name
  order by open_ratio desc"""
  result = graph.run(cql, {})
  return json.dumps(result.data())

