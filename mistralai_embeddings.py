import os

from time import sleep

import pandas as pd

from dotenv import load_dotenv
from mistralai.client import MistralClient
from neo4j import GraphDatabase, Result


load_dotenv()

def generate_embeddings(file_name, limit=None):

    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    )

    driver.verify_connectivity()

    query = """MATCH (m:Movie) WHERE m.plot IS NOT NULL
    RETURN m.movieId AS movieId, m.title AS title, m.plot AS plot"""

    if limit is not None:
        query += f" LIMIT {limit}"

    movies = driver.execute_query(
        query,
        result_transformer_=Result.to_df
    )

    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    
    embeddings = []

    for _, n in movies.iterrows():
        
        embeddings_response = client.embeddings(
            model="mistral-embed",
            input=[f"{n['title']}: {n['plot']}"],
        )
        sleep(1)

        embeddings.append({"movieId": n['movieId'], "embedding": embeddings_response.data[0].embedding})
        print(f"{n['movieId'] = }, {len(embeddings_response.data[0].embedding) = }")    

    embedding_df = pd.DataFrame(embeddings)
    embedding_df.head()
    embedding_df.to_csv(file_name, index=False)

if __name__ == "__main__":

    # generate_embeddings('./data/mistralai-embeddings.csv',limit=1)
    generate_embeddings('./data/mistralai-embeddings.csv',limit=1000)
