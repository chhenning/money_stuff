from dataclasses import asdict
from datetime import datetime
import json
import os
from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from dotenv import load_dotenv

from loguru import logger

import markdownify

from money_stuff.data_model import Newsletter, Article

load_dotenv()


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def parse_newsletter_html(html_content: str) -> List[Article]:
    """
    Parses the HTML content of a newsletter and extracts articles separated by <h2> tags.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    articles = []

    # headlines are <h2> tags
    headlines = soup.find_all("h2")

    for i, headline in enumerate(headlines):
        title = headline.get_text().strip()

        # The <h2> is often nested inside a table structure (td -> tr -> table).
        # We need to find the block element that contains the h2 and is a sibling of the content.
        # Based on analysis, the h2 is inside a table, and the content follows that table.
        header_block = headline.find_parent("table")
        if not header_block:
            # Fallback if structure is different
            header_block = headline

        # Collect content until the next headline or end of container
        content_parts = []
        curr = header_block.next_sibling

        while curr:
            # Check if this element is or contains the next headline
            if isinstance(curr, Tag):
                if curr.name == "h2" or curr.find("h2"):
                    break

            # Append sibling content
            if isinstance(curr, Tag):
                content_parts.append(str(curr))
            elif curr.string and curr.string.strip():
                content_parts.append(curr.string.strip())

            curr = curr.next_sibling

        html_body = "".join(content_parts)

        # Convert HTML to Markdown
        text_body = markdownify.markdownify(html_body, heading_style="ATX").strip()

        article = Article(title=title, text=text_body, html=html_body)
        articles.append(article)

    return articles


def process_emails(input_file: str, output_file: str):
    try:
        with open(input_file, "r") as f:
            raw_emails = json.load(f)
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        return
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from: {input_file}")
        return

    logger.info(f"Processing {len(raw_emails)} emails...")

    newsletters = []
    total_articles = 0

    for email_data in raw_emails:
        timestamp_str = email_data.get("timestamp")
        subject = email_data.get("subject")
        content = email_data.get("content")

        if not content:
            continue

        # Parse timestamp
        try:
            # Handle Z for UTC if present, though isoformat usually handles it
            sent_date = datetime.fromisoformat(timestamp_str)
        except (ValueError, TypeError):
            logger.warning(f"Could not parse timestamp for email: {subject}")
            continue

        articles = parse_newsletter_html(content)
        total_articles += len(articles)

        newsletter = Newsletter(sent_date=sent_date, subject=subject, articles=articles)
        newsletters.append(newsletter)

        if len(newsletters) % 100 == 0:
            logger.info(f"Processed {len(newsletters)} emails...")

    logger.info(f"Processed {len(newsletters)} newsletters.")
    logger.info(f"Extracted a total of {total_articles} articles.")

    # Verification: Print first newsletter's articles
    if newsletters:
        first_nl = newsletters[0]
        logger.info(f"--- Sample Newsletter: {first_nl.subject} ---")
        for art in first_nl.articles:
            logger.info(f"Article: {art.title}")

    # Convert to dicts for JSON serialization
    newsletters_dict = [asdict(nl) for nl in newsletters]

    logger.info(f"Saving parsed newsletters to {output_file}...")
    try:
        with open(output_file, "w") as f:
            json.dump(newsletters_dict, f, indent=4, default=json_serial)
        logger.info("Done.")
    except Exception as e:
        logger.error(f"Failed to save output: {e}")


if __name__ == "__main__":
    input_filename = os.getenv("EMAIL_JSON_OUT_FILENAME")
    output_filename = os.getenv("NEWSLETTER_JSON_OUT_FILENAME")

    process_emails(input_filename, output_filename)
