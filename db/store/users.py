import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.actions.user_stats as user_stats

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

def get_connection():
    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    print("Connection successful:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("DB connection error:", e)

def store_user(username: str, password: str, is_admin=False) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
        if cur.fetchone():
            return False

        cur.execute(
            "INSERT INTO users (username, password, admin) VALUES (%s, %s, %s);",
            (username, password, is_admin)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error storing user:", e)
        return False
    finally:
        cur.close()
        conn.close()

def validate_user(username: str, password: str) -> dict | None:
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s;",
            (username, password)
        )
        result = cur.fetchone()
        return result
    except Exception as e:
        print("Error validating user:", e)
        return None
    finally:
        cur.close()
        conn.close()

def add_watch_history(username: str, history: str) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor()

        history_str = ",".join(history)

        cur.execute(
            "UPDATE users SET watch_history = %s WHERE username = %s;",
            (history_str, username)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error updating watch history:", e)
        return False
    finally:
        cur.close()
        conn.close()


def get_watch_history(username: str) -> list:
    redis_data = user_stats.get_user_data(username)
    if redis_data and "watched_movies" in redis_data:
        return redis_data["watched_movies"]
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "SELECT watch_history FROM users WHERE username = %s;",
            (username,)
        )
        result = cur.fetchone()
        if result and result["watch_history"]:
            return [x.strip() for x in result["watch_history"].split(",")]
        return []
    except Exception as e:
        print("Error retrieving watch history:", e)
        return []
    finally:
        cur.close()
        conn.close()