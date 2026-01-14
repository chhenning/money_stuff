import sqlite3
import json
import os
from datetime import datetime

from dotenv import load_dotenv

from loguru import logger

load_dotenv()

DB_FILE = os.getenv("DB_FILENAME")
SQL_FILE = "sql/data_model.sql"
DATA_FILE = os.getenv("NEWSLETTER_JSON_OUT_FILENAME")


def init_db():
    if os.path.exists(DB_FILE):
        logger.info(f"Removing existing database at {DB_FILE}...")
        os.remove(DB_FILE)  # Start fresh for now, or use IF NOT EXISTS in SQL

    conn = sqlite3.connect(DB_FILE)
    with open(SQL_FILE, "r") as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()

    logger.info(f"Initialized database at {DB_FILE}.")
    return conn


def populate_db(conn):
    try:
        with open(DATA_FILE, "r") as f:
            newsletters = json.load(f)
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found.")
        return

    cursor = conn.cursor()

    count_newsletters = 0
    count_articles = 0

    for nl in newsletters:
        # Insert newsletter
        try:
            # sent_date is isoformat string in JSON, needs to be suitable for SQLite
            # SQLite doesn't have a native datetime type, typically ISO string is used
            cursor.execute(
                """
                INSERT OR IGNORE INTO newsletter (sent_date, subject)
                VALUES (?, ?)
            """,
                (nl["sent_date"], nl["subject"]),
            )

            # Check if inserted or ignored
            cursor.execute(
                "SELECT id FROM newsletter WHERE sent_date = ? AND subject = ?",
                (nl["sent_date"], nl["subject"]),
            )
            row = cursor.fetchone()
            if row:
                newsletter_id = row[0]
                count_newsletters += 1

                # Insert articles
                for art in nl.get("articles", []):
                    cursor.execute(
                        """
                        INSERT INTO article (newsletter_id, title, text)
                        VALUES (?, ?, ?)
                    """,
                        (newsletter_id, art["title"], art["text"]),
                    )
                    count_articles += 1

        except sqlite3.Error as e:
            logger.error(f"Error inserting newsletter {nl.get('subject')}: {e}")

    conn.commit()
    logger.info(
        f"Successfully inserted {count_newsletters} newsletters and {count_articles} articles."
    )


if __name__ == "__main__":
    conn = init_db()
    populate_db(conn)
    conn.close()
