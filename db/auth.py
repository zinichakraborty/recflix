import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

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

def store_user(username: str, password: str) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
        if cur.fetchone():
            return False

        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s);",
            (username, password)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error storing user:", e)
        return False
    finally:
        cur.close()
        conn.close()

def validate_user(username: str, password: str) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s;",
            (username, password)
        )
        result = cur.fetchone()
        return result is not None
    except Exception as e:
        print("Error validating user:", e)
        return False
    finally:
        cur.close()
        conn.close()