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

def openRatioByCategories():
  """returns JSON with columns open_ratio and name, rows are neighborhoods"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business)-[:CATEGORIZED_AS]-> (c:Category)
        with count(a) as total, c
        match (a:Business {is_open: 1}) -[:CATEGORIZED_AS]-> (c:Category)
        return (count(a)*1.0/total) as open_ratio, c.name as name
        order by open_ratio desc
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

def AvgStarNeighborhood():
  """returns JSON with columns stars and name, rows are neighborhoods"""
  neo4jUrl = "http://ec2-34-230-16-27.compute-1.amazonaws.com:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='123456')
  cql = """match (a:Business), (a) -[:LOCATED_IN]-> (b:Neighborhood)
        return avg(a.stars) as stars, b.name as name
        order by stars DESC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

def TotalVisitRegion():
  """returns JSON with columns name and visited, rows are neighborhoods"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), () - [r:REVIEWED] -> (a), (a) -[:LOCATED_IN]-> (b:Neighborhood)
        return b.name as name, count(*) as visited
        order by visited DESC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

def TopVisit():
  """returns JSON with columns name and visited"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), () - [r:REVIEWED] -> (a)
        return a.name as name, count(*) as visited
        order by visited DESC
        limit 10
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

def StoreNumRegion():
  """returns JSON with columns name and store, rows are neighborhoods"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), (a) -[:CATEGORIZED_AS]- (b:Category)
        return b.name as name, count(*) as store
        order by store DESC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

def AvgRateCategories():
  """returns JSON with columns name and store"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Category)
        return a.average as average, a.name as category
        order by a.average desc
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

def ResUp4StarsRegion():
  """returns JSON with columns stars and name, rows are restaurants"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), (a) -[:LOCATED_IN]-> (b:Neighborhood)
        where b.name = 'Shadyside' and (a.stars/a.count) > 4
        return (a.stars/a.count) as stars, a.name as name
        order by stars DESC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

def AvgRateYear():
  """returns JSON with columns name and avg_star, year"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), () -[r:REVIEWED]-> (a)
        return a.name as name, avg(a.stars/a.count) as avg_star, substring(r.date, 0, 4) as year
        order by name ASC, year ASC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())