from dotenv import load_dotenv
import os
import redis
import json

load_dotenv()
host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
password = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
    host=host,
    port=port,
    decode_responses=True,
    username="default",
    password=password,
)

def save_user_data(name, watched_movies, preferences):
    if not name:
        raise ValueError("User name is required")

    user_data = {
        "watched_movies": watched_movies,
        "preferences": preferences
    }

    r.set(name, json.dumps(user_data))
    print(f"Saved data for user: {name}")

def get_user_data(name):
    data = r.get(name)
    if data:
        return json.loads(data)
    else:
        print(f"No data found for user: {name}")
        return None

def get_all_user_data():
    all_keys = r.keys("*")
    all_data = {}

    for key in all_keys:
        data = r.get(key)
        try:
            all_data[key] = json.loads(data)
        except (TypeError, json.JSONDecodeError):
            all_data[key] = data

    return all_data