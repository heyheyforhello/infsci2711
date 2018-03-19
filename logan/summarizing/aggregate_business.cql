MATCH(b:Business)-[r:REVIEWED]-()
WITH b, COLLECT(r.stars) AS rlist, AVG(r.stars) AS average
SET b.average = average,
  b.starcount =
  [rs in
    [star in range(1,5) | filter(r IN rlist WHERE r = star)]
  | size(rs)];

MATCH(c:Category)<--(b:Business)
WITH c,
  COLLECT(b.starcount) AS starlist,
  SUM(b.average * b.reviews) AS total,
  SUM(b.reviews) AS num,
  COUNT(b) as cnt
SET
  c.average = total/num,
  c.reviews = num,
  c.businesses = cnt,
  c.starcount = REDUCE(stars = [0,0,0,0,0], s in starlist | [i in range(0,4) | stars[i] + s[i]]);

MATCH (c1:Category)<--(b:Business)-->(c2:Category)
WHERE c1 <> c2
WITH c1, c2, COUNT(b) AS num
MERGE (c1)-[:OVERLAPS{count: num}]-(c2);

MATCH(n:Neighborhood)<--(b:Business)
WITH n,
  COLLECT(b.starcount) AS starlist,
  SUM(b.average * b.reviews) AS total,
  SUM(b.reviews) AS num,
  COUNT(b) as cnt
SET
  n.average = total/num,
  n.reviews = num,
  n.businesses = cnt,
  n.starcount = REDUCE(stars = [0,0,0,0,0], s in starlist | [i in range(0,4) | stars[i] + s[i]]);

MATCH (n:Neighborhood)<--(b:Business)-->(c:Category)
WITH n, c,
    COLLECT(b.starcount) AS starlist,
  SUM(b.average * b.reviews) AS total,
  SUM(b.reviews) AS num,
  COUNT(b) as cnt
MERGE (n)-[i:CONTAINS]-(c)
ON CREATE SET
  i.average = total/num,
  i.reviews = num,
  i.businesses = cnt,
  i.starcount = REDUCE(stars = [0,0,0,0,0], s in starlist | [i in range(0,4) | stars[i] + s[i]]);
