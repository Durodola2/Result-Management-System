# auth.py
import sqlite3
from database import DB_NAME

def signup(matric, name, dept, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (matric, name, dept, password) VALUES (?, ?, ?, ?)",
            (matric, name, dept, password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception("Matric number already exists!")
    finally:
        conn.close()

def login(matric, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT matric, name, dept FROM users WHERE matric=? AND password=?", (matric, password))
    user = cursor.fetchone()
    conn.close()
    return user  # will return tuple (matric, name, dept) if found, else None