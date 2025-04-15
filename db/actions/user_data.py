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

def save_user_data(username, watched_movies, selected_genres, preferences):
    key = f"user:{username}"
    user_data = {
        "watched_movies": watched_movies,
        "selected_genres": selected_genres,
        "preferences": preferences
    }
    r.set(key, json.dumps(user_data))
    print(f"Saved data for {username}")

def get_user_data(username):
    key = f"user:{username}"
    data = r.get(key)
    if data:
        return json.loads(data)
    return None

def get_all_user_data():
    all_keys = r.keys("user:*")
    all_data = {}

    for key in all_keys:
        username = key.split(":")[1]
        data = r.get(key)
        try:
            all_data[username] = json.loads(data)
        except (TypeError, json.JSONDecodeError):
            all_data[username] = data

    return all_data

def delete_all_user_data():
    all_keys = r.keys("user:*")
    if not all_keys:
        print("No keys to delete.")
        return

    r.delete(*all_keys)
    print(f"Deleted {len(all_keys)} keys from Redis.")

if __name__ == "__main__":
    delete_all_user_data()