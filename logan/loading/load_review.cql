WITH $json AS JSON
UNWIND JSON.data AS input
WITH input AS data
MATCH (b:Business {business_id: data.business_id})
WHERE b IS NOT NULL
WITH data, b
MERGE (u:User {user_id: data.user_id})
MERGE (u) -[r:REVIEWED {review_id: data.review_id}]-> (b)
  ON CREATE SET
    r.stars = data.stars,
    r.date = data.date
RETURN count(r) AS count;

