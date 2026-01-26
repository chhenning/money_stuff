import sqlite3
import os
from dotenv import load_dotenv
from loguru import logger
from typing import List, Dict, Any

load_dotenv()

SQL_FILE = "sql/data_model.sql"
DB_FILE = os.getenv("DB_FILENAME", "")
assert DB_FILE


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


def get_db_connection():
    """Returns a sqlite3 connection object."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None


def init_ner_table():
    """Creates the article_ner table if it does not exist."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS article_ner (
                id           INTEGER PRIMARY KEY,
                article_id   INTEGER REFERENCES article(id) ON DELETE CASCADE,
                text         TEXT NOT NULL,
                label        TEXT NOT NULL,
                start_char   INTEGER NOT NULL,
                end_char     INTEGER NOT NULL
            )
        """
        )
        conn.commit()
        logger.info("Initialized article_ner table.")
    except sqlite3.Error as e:
        logger.error(f"Error creating article_ner table: {e}")
    finally:
        conn.close()


def get_all_articles() -> List[Dict[str, Any]]:
    """Loads all articles from the database."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, text FROM article")
        articles = [dict(row) for row in cursor.fetchall()]
        return articles
    except sqlite3.Error as e:
        logger.error(f"Error loading articles: {e}")
        return []
    finally:
        conn.close()


def get_all_ml_articles() -> List[Dict[str, Any]]:
    """Loads all articles from the database."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, ml_text FROM article")
        articles = [dict(row) for row in cursor.fetchall()]
        return articles
    except sqlite3.Error as e:
        logger.error(f"Error loading articles: {e}")
        return []
    finally:
        conn.close()


def save_entities(entities: List[Dict[str, Any]]):
    """Saves entities for a given article."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        data = [
            (
                ent["article_id"],
                ent["text"],
                ent["label"],
                ent["start_char"],
                ent["end_char"],
            )
            for ent in entities
        ]

        cursor.executemany(
            """
            INSERT INTO article_ner (article_id, text, label, start_char, end_char)
            VALUES (?, ?, ?, ?, ?)
            """,
            data,
        )

        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error saving entities: {e}")
    finally:
        conn.close()


def get_entities(article_id: int) -> List[Dict[str, Any]]:
    """Loads all entities for a given article from the database."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM article_ner WHERE article_id = ?", (article_id,))
        entities = [dict(row) for row in cursor.fetchall()]
        return entities
    except sqlite3.Error as e:
        logger.error(f"Error loading entities: {e}")
        return []
    finally:
        conn.close()
