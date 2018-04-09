WITH $json AS JSON
UNWIND JSON.data AS input
WITH input AS data
MATCH (b:Business {business_id: data.business_id})
WHERE b IS NOT NULL
WITH data, b
MERGE (u:User {user_id: data.user_id})
MERGE (u) -[t:TIPPED {text: data.text}]-> (b)
  ON CREATE SET
    t.likes = data.likes,
    t.date = data.date
RETURN count(t) AS count;

