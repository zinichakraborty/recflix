import os
from dotenv import load_dotenv
import json
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
from sentence_transformers import SentenceTransformer

load_dotenv()
uri = os.getenv("ZILLIZ_URI")
token = os.getenv("ZILLIZ_TOKEN")

connections.connect(uri=uri, token=token)

ef = SentenceTransformer("all-MiniLM-L6-v2")

fields = [
    FieldSchema(name="item_id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=256),
    FieldSchema(name="directedBy", dtype=DataType.VARCHAR, max_length=1024),
    FieldSchema(name="starring", dtype=DataType.VARCHAR, max_length=1024),
    FieldSchema(name="avgRating", dtype=DataType.FLOAT),
    FieldSchema(name="imdbId", dtype=DataType.VARCHAR, max_length=64),
    FieldSchema(name="title_embeddings", dtype=DataType.FLOAT_VECTOR, dim=384)
]

schema = CollectionSchema(fields=fields, description="Movie metadata collection with embeddings")
collection_name = "movies"
collection = Collection(name=collection_name, schema=schema)

file_path = "movie_dataset_public_final/raw/metadata_updated.json"
movie_data = []
with open(file_path, "r") as f:
    for line in f:
        obj = json.loads(line.strip())
        movie_data.append(obj)

movie_titles = [movie["title"] for movie in movie_data]
title_embeddings = ef.encode(movie_titles)

cleaned_data = [
    [movie["item_id"] for movie in movie_data],
    [movie["title"] for movie in movie_data],
    [movie["directedBy"] for movie in movie_data],
    [movie["starring"] for movie in movie_data],
    [movie["avgRating"] for movie in movie_data],
    [movie["imdbId"] for movie in movie_data],
    title_embeddings
]

BATCH_SIZE = 500

num_records = len(movie_data)
for i in range(0, num_records, BATCH_SIZE):
    batch = [
        cleaned_data[0][i:i+BATCH_SIZE],
        cleaned_data[1][i:i+BATCH_SIZE],
        cleaned_data[2][i:i+BATCH_SIZE],
        cleaned_data[3][i:i+BATCH_SIZE],
        cleaned_data[4][i:i+BATCH_SIZE],
        cleaned_data[5][i:i+BATCH_SIZE],
        cleaned_data[6][i:i+BATCH_SIZE],
    ]
    collection.insert(batch)

collection.flush()

collection.create_index(
    field_name="title_embeddings",
    index_params={"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
)

collection.load()

print("Data with embeddings stored successfully in Milvus.")