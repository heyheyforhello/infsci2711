WITH $json AS JSON
UNWIND JSON.data AS input
WITH input AS data
MATCH (u:User {user_id: data.user_id})
WHERE u IS NOT NULL
SET
  u.name = data.name,
  u.created = data.yelping_since,
  u.useful = data.useful,
  u.funny = data.funny,
  u.cool = data.cool,
  u.fans = data.fans,
  u.elite = data.elite,
  u.compliment_hot = data.compliment_hot,
  u.compliment_more = data.compliment_more,
  u.compliment_profile = data.compliment_profile,
  u.compliment_cute = data.compliment_cool,
  u.compliment_list = data.compliment_list,
  u.compliment_note = data.compliment_note,
  u.compliment_plain = data.compliment_plain,
  u.compliment_cool = data.compliment_cool,
  u.compliment_funny = data.compliment_funny,
  u.compliment_writer = data.compliment_writer,
  u.compliment_photos = data.compliment_photos
WITH u, data
UNWIND data.friends AS friend
  MATCH (u2:User {user_id: friend})
  WHERE u2 IS NOT NULL
  MERGE (u)-[:FRIENDS_WITH]-(u2)
RETURN COUNT(u) AS count;