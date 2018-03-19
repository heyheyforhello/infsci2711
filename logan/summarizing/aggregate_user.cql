MATCH (u:User)--()--(c:Category)
WITH u, COUNT(DISTINCT c) as total
SET u.categories = total

MATCH (u:User)--()--(n:Neighborhood)
WITH u, COUNT(DISTINCT n) as total
SET u.neighborhoods = total