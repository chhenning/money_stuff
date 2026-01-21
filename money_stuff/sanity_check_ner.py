import os
import sqlite3
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

DB_FILE = os.getenv("DB_FILENAME", "")

def check_ner_data():
    if not os.path.exists(DB_FILE):
        logger.error(f"Database file {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    logger.info("Starting NER sanity check...")

    try:
        # Join article_ner with article to get the source text
        cursor.execute("""
            SELECT 
                an.id as ner_id,
                an.article_id,
                an.text as recorded_text,
                an.start_char,
                an.end_char,
                a.ml_text
            FROM article_ner an
            JOIN article a ON an.article_id = a.id
        """)
        
        rows = cursor.fetchall()
        total_checked = len(rows)
        errors = []

        if total_checked == 0:
            logger.warning("No NER data found in the database.")
            return

        for row in rows:
            ner_id = row['ner_id']
            article_id = row['article_id']
            recorded_text = row['recorded_text']
            start = row['start_char']
            end = row['end_char']
            ml_text = row['ml_text']

            if ml_text is None:
                errors.append(f"NER ID {ner_id} (Article {article_id}): ml_text is NULL")
                continue

            # Check bounds
            if start < 0 or end > len(ml_text):
                errors.append(f"NER ID {ner_id} (Article {article_id}): Indices [{start}:{end}] out of bounds for text of length {len(ml_text)}")
                continue

            # Extract actual text from source
            actual_text = ml_text[start:end]

            print(actual_text)
            print(recorded_text)

            if actual_text != recorded_text:
                errors.append(
                    f"NER ID {ner_id} (Article {article_id}): Mismatch! "
                    f"Recorded: '{recorded_text}', Actual: '{actual_text}' "
                    f"at [{start}:{end}]"
                )

        if not errors:
            logger.success(f"Sanity check passed! Verified {total_checked} entities.")
        else:
            logger.error(f"Sanity check failed with {len(errors)} errors out of {total_checked} checked.")
            for e in errors[:20]:  # Show first 20 errors
                logger.error(f"  - {e}")
            if len(errors) > 20:
                logger.error(f"  ... and {len(errors) - 20} more.")

    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_ner_data()
