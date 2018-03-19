MATCH (c:Category)
RETURN c.name, c.businesses, c.reviews, c.average
ORDER BY c.businesses DESC;
