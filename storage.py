import sqlite3
from sqlite3 import Connection

def init_db(path="data.db") -> Connection:
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS scripts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        title TEXT,
        hook TEXT,
        main_points TEXT,
        script TEXT,
        description TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    return conn

def save_script(conn, topic: str, doc: dict):
    c = conn.cursor()
    c.execute("""
        INSERT INTO scripts (topic, title, hook, main_points, script, description, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        topic,
        doc.get("title", ""),
        doc.get("hook", ""),
        "\n".join(doc.get("main_points", [])) if isinstance(doc.get("main_points"), list) else str(doc.get("main_points")),
        doc.get("script", ""),
        doc.get("description", ""),
        ",".join(doc.get("tags", [])) if isinstance(doc.get("tags"), list) else str(doc.get("tags"))
    ))
    conn.commit()
    return c.lastrowid
