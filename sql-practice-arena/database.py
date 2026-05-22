import sqlite3
import pandas as pd
import os

DB_PATH = 'practice.db'

def get_connection():
    """Returns a new connection to the SQLite database."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def execute_query(query: str):
    """Executes a SELECT query and returns a pandas DataFrame, or error message."""
    conn = get_connection()
    try:
        # read_sql_query is perfect for SELECT statements
        # For non-SELECT (like INSERT/UPDATE/DELETE), read_sql_query might fail
        # but since this is practice, we mostly expect SELECT.
        # Let's handle non-SELECT gracefully.
        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")):
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return pd.DataFrame([{"Status": "Success", "Rows Affected": cursor.rowcount}])
        
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def get_schema():
    """Returns a dictionary mapping table names to a list of their columns."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema = {}
    for table in tables:
        # Get columns for each table
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [row[1] for row in cursor.fetchall()]
        schema[table] = columns
        
    conn.close()
    return schema
