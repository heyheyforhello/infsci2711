WITH $json AS JSON
UNWIND JSON.data AS input
WITH input AS data
MATCH (b:Business {business_id: data.business_id}), (u:User {user_id: data.user_id})
WHERE b IS NOT NULL AND u IS NOT NULL
WITH data, b, u
MERGE (u) -[r:REVIEW]-> (b)
  ON CREATE SET
    r.stars = data.stars
RETURN count(r) AS count;