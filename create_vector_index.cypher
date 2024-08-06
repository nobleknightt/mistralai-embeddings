CREATE VECTOR INDEX `moviePlots` IF NOT EXISTS
FOR (n: Movie) ON (n.embedding)
OPTIONS {indexConfig: {
 `vector.dimensions`: 1024,
 `vector.similarity_function`: 'cosine'
}};
