import py2neo
import json

# What is the ratio of stores remain open/ total in different regions?
def openRatioByRegion():
  """returns JSON with columns open_ratio and name, rows are neighborhoods"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business)-[:LOCATED_IN]-> (c:Neighborhood)
  with count(a) as total, c
  match (a:Business {is_open: 1}) -[:LOCATED_IN]-> (c:Neighborhood)
  return (count(a)*1.0/total) as barValue, c.name as barLabel
  order by barValue desc"""
  result = graph.run(cql, {})
  return json.dumps(result.data())

# What is the ratio of stores remain open/ total in different categories?
def openRatioByCategories():
  """returns JSON with columns open_ratio and name, rows are neighborhoods"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business)-[:CATEGORIZED_AS]-> (c:Category)
        with count(a) as total, c
        match (a:Business {is_open: 1}) -[:CATEGORIZED_AS]-> (c:Category)
        return (count(a)*1.0/total) as barValue, c.name as barLabel
        order by barValue desc
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# For stores from different neighborhood, what is the average yelp given stars?
def AvgStarNeighborhood():
  """returns JSON with columns stars and name, rows are neighborhoods"""
  neo4jUrl = "http://ec2-34-230-16-27.compute-1.amazonaws.com:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='123456')
  cql = """match (a:Business), (a) -[:LOCATED_IN]-> (b:Neighborhood)
        return avg(a.stars) as barValue, b.name as barLabel
        order by barValue DESC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# What is the total costumer visit count for stores reside in different regions?
def TotalVisitRegion():
  """returns JSON with columns name and visited, rows are neighborhoods"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), () - [r:REVIEWED] -> (a), (a) -[:LOCATED_IN]-> (b:Neighborhood)
        return b.name as barLabel, count(*) as barValue
        order by barValue DESC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# What is the most visited top-20 business brand?
def TopVisit():
  """returns JSON with columns name and visited"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), () - [r:REVIEWED] -> (a)
        return a.name as barLabel, count(*) as barValue
        order by barValue DESC
        limit 20
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# What is the total numbers of business store in each category?
def StoreNumRegion():
  """returns JSON with columns name and store, rows are neighborhoods"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), (a) -[:CATEGORIZED_AS]- (b:Category)
        return b.name as barLabel, count(*) as barValue
        order by barLabel DESC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# What is the average ratings of different category?
def AvgRateCategories():
  """returns JSON with columns name and store"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Category)
        return a.average as barValue, a.name as barLabel
        order by barValue desc
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# What restaurant rated more than 4 stars in a certain neighborhood? (example: Shadyside)
def ResUp4StarsRegion():
  """returns JSON with columns stars and name, rows are restaurants"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:Business), (a) -[:LOCATED_IN]-> (b:Neighborhood)
        where b.name = 'Shadyside' and (a.stars/a.count) > 4
        return (a.stars/a.count) as barValue, a.name as barLabel
        order by barValue DESC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# What is the average rating in each year?
def AvgRateYear():
  """returns JSON with columns name and avg_star, year"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match () -[r:REVIEWED]-> ()
        return avg(r.stars) as barValue, substring(r.date, 0, 4) as barLabel
        order by barLabel ASC
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())


# What is the count of ratings and average rating of stores in each neighborhood in a certain year?(example:2017)
def AvgRateYearRegion():
  """returns JSON with columns name and avg_star, region"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match ()-[r:REVIEWED]->()-[:LOCATED_IN]->(a:Neighborhood)
        where substring(r.date, 0, 4) = '2017'
        return avg(r.stars) as barValue, a.name as barLabel
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# What is the top 20 categories with total costumer visited?
def TopVisitStoreCategories():
  """returns JSON with columns name and visited, category"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match ()-[r:REVIEWED]->()-[:CATEGORIZED_AS]->(a:Category)
        return count(*) as barValue, a.name as barLabel
        order by barValue desc
        limit 20
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())

# Is there a relation between average star given from a user and the user’s created day?
def UserRateYear():
  """returns JSON with columns name and avg_star, created_year"""
  neo4jUrl = "http://18.219.142.86:7474/db/data"
  graph = py2neo.Graph(neo4jUrl, password='password')
  cql = """match (a:User) -[r:REVIEWED]-> ()
        return avg(r.stars) as barValue, substring(a.created, 0, 4) as barLabel
        order by barLabel asc
        """
  result = graph.run(cql, {})
  return json.dumps(result.data())
