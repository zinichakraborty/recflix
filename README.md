# Recflix

## Installation

```bash
conda env create -f environment.yml
```

Then,

```bash
conda activate recflix-env
```

## ENVIRONMENT VARIABLES

1. Create a free Zilliz (Milvus Cloud), Supabase, and Redis Cloud account/cluster.
2. In Supabase create a `users` table that holds id, username (text, unique, not null), and password (text, not null).
3. Create a .env file and add these keys:

```bash
#Redis
REDIS_HOST=''
REDIS_PORT=''
REDIS_PASSWORD=''

#Supabase
user=''
password=''
host=''
port=''
dbname=postgres

#Milvus
ZILLIZ_URI=''
ZILLIZ_TOKEN=''
```

## Movie Database

To populate the movie vector database:

1. Download the dataset below and add folder (should not commit due to gitignore)
2. Run (should take 5-10 minutes each):

```bash
python db/store/movies.py
python db/store/tags.py
```

## Dataset

Dataset download link: https://grouplens.org/datasets/movielens/tag-genome-2021/

## Run App

Streamlit:

```bash
streamlit run app/main.py
```
