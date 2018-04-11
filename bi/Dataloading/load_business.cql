WITH $json AS JSON
UNWIND JSON.data AS input
WITH input AS data
MERGE (b:Business {business_id: data.business_id})
  ON CREATE SET
    b.name = data.name,
    b.review_count = data.review_count,
    b.stars = data.stars,
    b.is_open = data.is_open
FOREACH (cat IN data.categories |
  MERGE (c:Category {name: cat})
  MERGE (b)-[:CATEGORIZED_AS]->(c))
WITH data, b
WHERE data.neighborhood IS NOT NULL
MERGE (n:Neighborhood {name: data.neighborhood})
MERGE (b) -[:LOCATED_IN]-> (n)
RETURN COUNT(b) AS count;