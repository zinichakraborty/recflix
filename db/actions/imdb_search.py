import requests
import os
from dotenv import load_dotenv

def search_movies(query):
    load_dotenv()

    api_key = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": query,
        "include_adult": False,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [movie["title"] for movie in data.get("results", [])]
    return []