WITH $json AS JSON
UNWIND JSON.data AS input
WITH input AS data
MERGE (c:Checkin)
  ON CREATE SET
    c.business_id = data.business_id,
    c.day_of_week = data.day_of_week,
    c.count = data.count
RETURN count(c) AS count;