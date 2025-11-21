import sqlite3
import json

def init_db():
    conn = sqlite3.connect("lost_found.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lost_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        embedding TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS found_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        embedding TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_item(table, name, desc, embed):
    conn = sqlite3.connect("lost_found.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {table} (name, description, embedding) VALUES (?, ?, ?)",
                (name, desc, json.dumps(embed)))
    conn.commit()
    conn.close()


def fetch_all(table):
    conn = sqlite3.connect("lost_found.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    data = cur.fetchall()
    conn.close()
    return data
