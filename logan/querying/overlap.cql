MATCH (c:Category)
WITH c ORDER BY c.businesses DESC LIMIT 20
MATCH (c2:Category)
WHERE c2.name IN $category
OPTIONAL MATCH (c)-[o:OVERLAPS]-(c2)
RETURN c.name, o.count ORDER BY c.businesses DESC
