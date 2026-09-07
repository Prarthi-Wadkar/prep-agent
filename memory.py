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
    """topics: list of (topic, category, initial_status). Safe to call repeatedly - existing rows are left untouched (INSERT or IGNORE)"""
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM topics where status = 'weak" ORDER BY last_tested ASC LIMIT ?", (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_topics(db_path: str =DB_PATH):
    conn = get_connection(db_path)
    rows = conn.execute("SELECT * FROM topics ORDER BY status, topic").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def log_session(topic, question, answer_given, correct, time_taken_seconds, db_path: str = DB_PATH):
    conn = get_connection(db_path)
    conn.execute(
        """INSERT INTO sessions
           (timestamp, topic, question, answer_given, correct, time_taken_seconds)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (datetime.now().isoformat(), topic, question, answer_given, int(correct), time_taken_seconds),
    )
    conn.commit()
    conn.close()


def update_topic_status(topic, new_status, note, db_path: str = DB_PATH):
    conn = get_connection(db_path)
    conn.execute(
        """UPDATE topics SET status = ?, notes = ?, last_tested = ?,
           times_tested = times_tested + 1 WHERE topic = ?""",
        (new_status, note, datetime.now().isoformat(), topic),
    )
    conn.commit()
    conn.close()