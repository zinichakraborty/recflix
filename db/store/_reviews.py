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
    FieldSchema(name="txt", dtype=DataType.VARCHAR, max_length=8192),
    FieldSchema(name="txt_embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
]
schema = CollectionSchema(fields=fields, description="Reviews collections with embeddings")
collection_name = "reviews"

collection = Collection(name=collection_name, schema=schema)

file_path = "movie_dataset_public_final/raw/reviews.json"
text_data = []
with open(file_path, "r") as f:
    for line in f:
        obj = json.loads(line.strip())
        text_data.append(obj)

texts = [entry["txt"] for entry in text_data]
embeddings = ef.encode(texts).tolist()

cleaned_data = [
    [entry["item_id"] for entry in text_data],
    texts,
    embeddings,
]

BATCH_SIZE = 500
num_records = len(text_data)
for i in range(0, num_records, BATCH_SIZE):
    batch = [
        cleaned_data[0][i:i+BATCH_SIZE],
        cleaned_data[1][i:i+BATCH_SIZE],
        cleaned_data[2][i:i+BATCH_SIZE],
    ]
    collection.insert(batch)

collection.flush()
collection.create_index(
    field_name="txt_embedding",
    index_params={"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}},
)
collection.load()

print("Reviews data with embeddings stored successfully in Milvus.")