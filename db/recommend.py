import os
from dotenv import load_dotenv
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer

def recommend_movies(query):
    load_dotenv()

    connections.connect(
        uri=os.getenv("ZILLIZ_URI"),
        token=os.getenv("ZILLIZ_TOKEN")
    )

    model = SentenceTransformer("all-MiniLM-L6-v2")

    collection_name = "movies"
    collection = Collection(name=collection_name)
    collection.load()

    query_embedding = model.encode([query]).tolist()

    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    results = collection.search(
        data=query_embedding,
        anns_field="title_embeddings",
        param=search_params,
        limit=10,
        output_fields=["title", "directedBy", "starring", "avgRating", "imdbId"]
    )

    return [
        {
            "title": hit.entity.title,
            "avgRating": hit.entity.avgRating,
            "directedBy": hit.entity.directedBy,
            "starring": hit.entity.starring,
            "imdbId": hit.entity.imdbId,
        }
        for hit in results[0]
    ]