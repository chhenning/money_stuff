import os
import sqlite3

from dotenv import load_dotenv

import pandas as pd

load_dotenv()

DB_FILE = os.getenv("DB_FILENAME", "")


def db_stats():
    try:
        conn = sqlite3.connect(DB_FILE)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return

    print("--- Database Statistics ---\n")

    # 1. Total Counts
    try:
        df_newsletters = pd.read_sql_query("SELECT * FROM newsletter", conn)
        df_articles = pd.read_sql_query("SELECT * FROM article", conn)

        print(f"Total Newsletters: {len(df_newsletters)}")
        print(f"Total Articles:    {len(df_articles)}")
    except Exception as e:
        print(f"Error reading data: {e}")
        conn.close()
        return

    # 2. Date Range
    if not df_newsletters.empty:
        # Converting sent_date to datetime objects for accurate min/max finding
        # Handling potential ISO format differences or errors
        df_newsletters["sent_date"] = pd.to_datetime(
            df_newsletters["sent_date"], errors="coerce"
        )

        min_date = df_newsletters["sent_date"].min()
        max_date = df_newsletters["sent_date"].max()
        print(f"Date Range:        {min_date} to {max_date}")

    # 3. Validating Article Links
    # Join articles with newsletters to get newsletter info for each article
    df_merged = pd.merge(
        df_articles,
        df_newsletters,
        left_on="newsletter_id",
        right_on="id",
        suffixes=("_art", "_news"),
    )

    # 4. Articles per Newsletter stats
    articles_per_nl = df_articles.groupby("newsletter_id").size()
    print(f"Avg Articles/NL:   {articles_per_nl.mean():.2f}")
    print(f"Max Articles/NL:   {articles_per_nl.max()}")
    print(f"Min Articles/NL:   {articles_per_nl.min()}")

    # 5. Word Counts
    # Simple word count approximation by splitting on space
    df_articles["word_count"] = df_articles["text"].apply(lambda x: len(str(x).split()))

    print(f"\nAvg Word Count/Article: {df_articles['word_count'].mean():.2f}")

    # 6. Top 5 Longest Articles
    print("\n--- Top 5 Longest Articles ---")
    top_5 = df_articles.nlargest(5, "word_count")
    for index, row in top_5.iterrows():
        print(f"{row['word_count']} words | {row['title']}")

    conn.close()
