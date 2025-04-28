import os
from dotenv import load_dotenv
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
import numpy as np

def recommend_movies(watched, genre, query, min_rating, include_watch_history):
    load_dotenv()

    connections.connect(
        uri=os.getenv("ZILLIZ_URI"),
        token=os.getenv("ZILLIZ_TOKEN")
    )

    model = SentenceTransformer("all-MiniLM-L6-v2")

    tag_collection = Collection(name="tags")
    tag_collection.load()

    if include_watch_history and watched:
        query_embedding = weighted_mean_embedding(
            query=query,
            genre=genre,
            watched_embeddings=get_tag_embeddings_for_movies(watched),
            model=model,
            weights={
                "query": 0.5,
                "genre": 0.2,
                "watched": 0.3
            }
        )
    else:
        query_embedding = weighted_mean_embedding_basic(
            query=query,
            genre=genre,
            model=model,
            weights={
                "query": 0.7,
                "genre": 0.3
            }
        )

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

def get_tag_embeddings_for_movies(movie_titles: list[str]):
    load_dotenv()

    connections.connect(
        uri=os.getenv("ZILLIZ_URI"),
        token=os.getenv("ZILLIZ_TOKEN")
    )

    movies_collection = Collection(name="movies")
    movies_collection.load()

    formatted_titles = [f'"{title}"' for title in movie_titles]
    expr = f'title in [{", ".join(formatted_titles)}]'
    movie_entries = movies_collection.query(
        expr=expr,
        output_fields=["item_id"]
    )

    if not movie_entries:
        return []

    item_ids = [entry["item_id"] for entry in movie_entries]

    tags_collection = Collection(name="tags")
    tags_collection.load()

    expr = f"item_id in [{', '.join(map(str, item_ids))}]"
    tag_entries = tags_collection.query(
        expr=expr,
        output_fields=["tags_embedding"]
    )

    return [entry["tags_embedding"] for entry in tag_entries]

def weighted_mean_embedding(query, genre, watched_embeddings, model, weights):
    query_vector = np.array(model.encode(query)).flatten()

    if isinstance(genre, list):
        if genre:
            genre_vector = np.mean(np.array(model.encode(genre)), axis=0)
        else:
            genre_vector = np.zeros_like(query_vector)
    else:
        genre_vector = np.array(model.encode(genre)).flatten()

    combinged_vectors = []
    combined_weights = []

    combinged_vectors.append(query_vector)
    combined_weights.append(weights["query"])

    combinged_vectors.append(genre_vector)
    combined_weights.append(weights["genre"])

    for vector in watched_embeddings:
        vector = np.array(vector).flatten()
        combinged_vectors.append(vector)
        combined_weights.append(weights["watched"] / len(watched_embeddings))

    combinged_vectors = np.stack(combinged_vectors)
    combined_weights = np.array(combined_weights).reshape(-1, 1)

    weighted_avg = np.sum(combinged_vectors * combined_weights, axis=0) / np.sum(combined_weights)
    return [weighted_avg.tolist()]

def weighted_mean_embedding_basic(query, genre, model, weights):
    query_vector = np.array(model.encode(query))
    if isinstance(genre, list):
        if genre:
            genre_vector = np.array(model.encode(genre))
            genre_vector = np.mean(genre_vector, axis=0)
        else:
            genre_vector = np.zeros_like(query_vector)
    else:
        genre_vector = np.array(model.encode(genre))
    
    combinged_vectors = np.stack([query_vector, genre_vector])
    combined_weights = np.array([weights["query"], weights["genre"]]).reshape(-1, 1)
    
    weighted_avg = np.sum(combinged_vectors * combined_weights, axis=0) / np.sum(combined_weights)
    return [weighted_avg.tolist()]