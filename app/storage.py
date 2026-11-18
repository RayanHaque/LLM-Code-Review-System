import json
import os
import sqlite3
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

def get_db_path():
    return Path(os.getenv("REVIEW_DB_PATH", "storage/reviews.db"))

def connection():
    path = get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connection() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS reviews (
            id TEXT PRIMARY KEY, language TEXT NOT NULL, code TEXT NOT NULL,
            result TEXT NOT NULL, mode TEXT NOT NULL, created_at TEXT NOT NULL)""")

def save_review(language, code, result, mode):
    review_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    with connection() as con:
        con.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?)",
                    (review_id, language, code, json.dumps(result), mode, created_at))
    return {"id": review_id, "language": language, "result": result,
            "mode": mode, "created_at": created_at}

def list_reviews():
    with connection() as con:
        rows = con.execute("SELECT id, language, mode, created_at FROM reviews ORDER BY created_at DESC LIMIT 50").fetchall()
    return [dict(row) for row in rows]

def get_review(review_id):
    with connection() as con:
        row = con.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
    if row is None:
        return None
    item = dict(row)
    item["result"] = json.loads(item["result"])
    return item
