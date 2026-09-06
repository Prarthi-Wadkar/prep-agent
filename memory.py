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
        ststus TEXT DEFAULT 'untested', -- weak | solid | untested
        )

        """
    )