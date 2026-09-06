import sqlite3
from datetime import datetime

DB_PATH = "prep_agent.db"

def get_connection(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS topics(
        topic TEXT PRIMARY KEY,
        category TEXT,
        status TEXT DEFAULT 'untested', -- weak | solid | untested
        notes TEXT DEFAULT '',
        times_tested INTEGER DEFAULT 0,
        last_tested TEXT
        )
        """
    )
    conn.execute(
        """  CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            topic TEXT,
            question TEXT,
            answer_given TEXT,
            correct INTEGER,
            time_taken_seconds REAL
        )
        """
    )
    conn.commit()
    conn.close()


def seed_topics(topics: list[tuple[str,str,str]], db_path: str = DB_PATH):
    """topics: list of (topic, category, initial_status). Safe to call repeatedly"""