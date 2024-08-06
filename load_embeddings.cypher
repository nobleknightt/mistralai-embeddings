LOAD CSV WITH HEADERS
FROM 'https://raw.githubusercontent.com/nobleknightt/mistralai-embeddings/main/data/mistralai-embeddings.csv'
AS row
MATCH (m:Movie {movieId: row.movieId})
CALL db.create.setNodeVectorProperty(m, 'embedding', apoc.convert.fromJsonList(row.embedding))
RETURN count(*);
