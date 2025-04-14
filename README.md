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
1. Create a free Zilliz (Milvus Cloud) and Redis Cloud account/cluster.
2. Create a .env file and add these keys:
```bash
REDIS_HOST=''
REDIS_PORT=''
REDIS_PASSWORD=''

ZILLIZ_URI=''
ZILLIZ_TOKEN=''
```
## Run App
Streamlit:
```bash
streamlit run app/main.py
```
## Movie Database
VectorDB hosted on Milvus

## User Profile Storage
Redis

## Dataset
Download the dataset: https://grouplens.org/datasets/movielens/tag-genome-2021/
