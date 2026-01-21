import sqlite3
import json
import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv

from loguru import logger

from money_stuff.data_model import Newsletter
from money_stuff.utils import clean_markdown_for_ml

load_dotenv()

DB_FILE = os.getenv("DB_FILENAME", "")

DATA_FILE = os.getenv("NEWSLETTER_JSON_OUT_FILENAME", "")


def populate_db(conn, newsletters: List[Newsletter]):

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
                (nl.sent_date, nl.subject),
            )

            # Check if inserted or ignored
            cursor.execute(
                "SELECT id FROM newsletter WHERE sent_date = ? AND subject = ?",
                (nl.sent_date, nl.subject),
            )
            row = cursor.fetchone()
            if row:
                newsletter_id = row[0]
                count_newsletters += 1

                # Insert articles
                for art in nl.articles:
                    cursor.execute(
                        """
                        INSERT INTO article (newsletter_id, title, text, ml_text)
                        VALUES (?, ?, ?, ?)
                    """,
                        (
                            newsletter_id,
                            art.title,
                            art.text,
                            clean_markdown_for_ml(art.text),
                        ),
                    )
                    count_articles += 1

        except sqlite3.Error as e:
            logger.error(f"Error inserting newsletter {nl.subject}: {e}")

    conn.commit()
    logger.info(
        f"Successfully inserted {count_newsletters} newsletters and {count_articles} articles."
    )
