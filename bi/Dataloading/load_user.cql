WITH $json AS JSON
UNWIND JSON.data AS input
WITH input AS data
MERGE (u:User {user_id: data.user_id})
  ON CREATE SET
    u.yelping_since = data.yelping_since,
    u.review_count = data.review_count,
    u.average_stars = data.average_stars
WITH u, data
UNWIND data.friends AS friend
  MATCH (u2:User {user_id: friend})
  WHERE u2 IS NOT NULL
  MERGE (u)-[:FRIEND]-(u2)
RETURN COUNT(u) AS count;