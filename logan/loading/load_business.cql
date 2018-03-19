WITH $json AS JSON
UNWIND JSON.data AS input
WITH input AS data
WHERE data.city = "Pittsburgh" AND data.state = "PA"
MERGE (s:State {code: data.state})
MERGE (c:City {name: data.city}) -[:LOCATED_IN]-> (s)
MERGE (b:Business {business_id: data.business_id})
  ON CREATE SET
    b.name = data.name,
    b.address = data.address,
    b.zip = data.`postal code`,
    b.lat = data.latitutde,
    b.long = data.longitude,
    b.is_open = data.is_open
MERGE (b) -[:LOCATED_IN]-> (c)
FOREACH (cat IN data.categories |
  MERGE (c:Category {name: cat})
  MERGE (b)-[:CATEGORIZED_AS]->(c))
WITH data, b, c
WHERE data.neighborhood IS NOT NULL
MERGE (n:Neighborhood {name: data.neighborhood}) -[:LOCATED_IN]-> (c)
MERGE (b) -[:LOCATED_IN]-> (n)
RETURN COUNT(b) AS count;
