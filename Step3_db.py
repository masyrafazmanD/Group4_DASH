import sqlite3
import json

DB_NAME = "exchange.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base TEXT,
            target TEXT,
            rate REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_db(data: dict) -> dict:

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO records (base, target, rate) VALUES (?, ?, ?)",
        (data["base"], data["target"], data["rate"])
    )

    conn.commit()

    record_id = cursor.lastrowid

    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    record = cursor.fetchone()

    conn.close()

    return dict(record)

if __name__ == "__main__":
    from Step1_scrap import scrap_data

    init_db()

    data = scrap_data()
    saved_record = save_db(data)
    print(json.dumps(saved_record, indent=2))