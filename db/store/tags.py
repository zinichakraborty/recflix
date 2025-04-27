import os
from dotenv import load_dotenv
import json
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
from sentence_transformers import SentenceTransformer
from collections import defaultdict

load_dotenv()
uri = os.getenv("ZILLIZ_URI")
token = os.getenv("ZILLIZ_TOKEN")

connections.connect(uri=uri, token=token)

embedding = SentenceTransformer("all-MiniLM-L6-v2")

fields = [
    FieldSchema(name="item_id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="tags", dtype=DataType.VARCHAR, max_length=4096),
    FieldSchema(name="tags_embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
]

schema = CollectionSchema(fields=fields, description="Tag associations per movie with embeddings")
collection_name = "tags"

collection = Collection(name=collection_name, schema=schema)

with open("movie_dataset_public_final/raw/tags.json", "r") as f:
    tag_id_map = {}
    for line in f:
        tag_item = json.loads(line.strip())
        tag_id_map[tag_item["id"]] = tag_item["tag"]

movie_tag_map = defaultdict(list)
with open("movie_dataset_public_final/raw/tag_count.json", "r") as f:
    for line in f:
        movie_tag = json.loads(line.strip())
        tag_id = movie_tag["tag_id"]
        tag = tag_id_map.get(tag_id)
        if tag:
            movie_tag_map[movie_tag["item_id"]].append(tag)

item_ids = []
tag_strings = []
tag_embeddings = []

for item_id, tags in movie_tag_map.items():
    tags_str = ", ".join(tags)
    item_ids.append(item_id)
    tag_strings.append(tags_str)
    tag_embeddding = embedding.encode(tags_str).tolist()
    tag_embeddings.append(tag_embeddding)

BATCH_SIZE = 500
num_records = len(item_ids)
for i in range(0, num_records, BATCH_SIZE):
    batch = [
        item_ids[i:i+BATCH_SIZE],
        tag_strings[i:i+BATCH_SIZE],
        tag_embeddings[i:i+BATCH_SIZE],
    ]
    collection.insert(batch)

collection.flush()
collection.create_index(
    field_name="tags_embedding",
    index_params={"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}},
)
collection.load()

print("Tag associations with embeddings stored successfully in Milvus.")