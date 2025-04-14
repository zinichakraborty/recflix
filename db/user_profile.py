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

def save_user_data(name, watched_movies, selected_genres, preferences):
    if not name:
        raise ValueError("User name is required")

    user_data = {
        "watched_movies": watched_movies,
        "selected_genres": selected_genres,
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

def delete_all_user_data():
    all_keys = r.keys("*")
    if not all_keys:
        print("No keys to delete.")
        return

    r.delete(*all_keys)
    print(f"Deleted {len(all_keys)} keys from Redis.")

if __name__ == "__main__":
    delete_all_user_data()