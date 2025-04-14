import os
from dotenv import load_dotenv
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer

def recommend_movies(query, min_rating):
    load_dotenv()

    connections.connect(
        uri=os.getenv("ZILLIZ_URI"),
        token=os.getenv("ZILLIZ_TOKEN")
    )

    model = SentenceTransformer("all-MiniLM-L6-v2")

    tag_collection = Collection(name="tags")
    tag_collection.load()

    query_embedding = model.encode([query]).tolist()

    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    results = tag_collection.search(
        data=query_embedding,
        anns_field="tags_embedding",
        param=search_params,
        limit=20,
        output_fields=["item_id"]
    )

    item_ids = [hit.entity.item_id for hit in results[0]]
    scores = [hit.distance for hit in results[0]] 

    movies_collection = Collection(name="movies")
    movies_collection.load()

    expr = f"item_id in [{', '.join(map(str, item_ids))}] and avgRating >= {min_rating}"
    movie_results = movies_collection.query(
        expr=expr,
        output_fields=["item_id", "title", "avgRating", "directedBy", "starring", "imdbId"]
    )

    id_to_movie = {movie["item_id"]: movie for movie in movie_results}
    ordered_movies = [{"movie": id_to_movie[iid], "score": score} for iid, score in zip(item_ids, scores) if iid in id_to_movie]

    return ordered_movies