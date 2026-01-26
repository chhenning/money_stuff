import os
import sys
from pathlib import Path
from loguru import logger

from money_stuff import get_db_connection
from money_stuff.utils import clean_markdown_from_links


def download_article(article_id: int = 1, output_dir: str = "data"):
    """
    Downloads a single article from the database and saves it as a markdown file.
    """
    conn = get_db_connection()
    if not conn:
        logger.error("Could not connect to the database.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, text FROM article WHERE id = ?", (article_id,))
        row = cursor.fetchone()

        if not row:
            logger.warning(f"No article found with ID {article_id}.")
            return

        article = dict(row)
        title = article["title"]
        text = article["text"]
        
        text = clean_markdown_from_links(text)
        
        # Simple sanitization for filename
        safe_title = "".join([c if c.isalnum() else "_" for c in title])[:50]
        filename = f"article_{article_id}_{safe_title}.md"
        output_path = Path(output_dir) / filename
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(text)

        logger.success(f"Article '{title}' saved to {output_path}")

    except Exception as e:
        logger.error(f"Error downloading article: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Check if an ID was passed as an argument, otherwise default to 1
    target_id = 1
    if len(sys.argv) > 1:
        try:
            target_id = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid article ID: {sys.argv[1]}")
            sys.exit(1)

    download_article(target_id)
