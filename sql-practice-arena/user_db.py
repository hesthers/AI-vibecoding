import sqlite3
import pandas as pd
from datetime import datetime
import os

USER_DB_PATH = 'user_data.db'

def init_user_db():
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    # History table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            theme TEXT,
            question_title TEXT,
            query TEXT,
            status TEXT
        )
    ''')
    # Favorites table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            theme TEXT,
            question_title TEXT,
            query TEXT,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_history(theme, question_title, query, status):
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO history (timestamp, theme, question_title, query, status) VALUES (?, ?, ?, ?, ?)",
        (timestamp, theme, question_title, query, status)
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(USER_DB_PATH)
    df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
    conn.close()
    return df

def add_favorite(theme, question_title, query, note=""):
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO favorites (timestamp, theme, question_title, query, note) VALUES (?, ?, ?, ?, ?)",
        (timestamp, theme, question_title, query, note)
    )
    conn.commit()
    conn.close()

def get_favorites():
    conn = sqlite3.connect(USER_DB_PATH)
    df = pd.read_sql_query("SELECT * FROM favorites ORDER BY id DESC", conn)
    conn.close()
    return df

def remove_favorite(fav_id):
    conn = sqlite3.connect(USER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
    conn.commit()
    conn.close()

# Initialize on module load
init_user_db()
