from datetime import datetime
import os

from dotenv import load_dotenv

import pandas as pd

import sqlite3

import streamlit as st

load_dotenv()


DB_FILE = os.getenv("DB_FILENAME")


def get_connection():
    return sqlite3.connect(DB_FILE)


def main():
    st.set_page_config(page_title="Money Stuff Explorer", layout="wide")
    st.title("Money Stuff Newsletter Explorer")

    conn = get_connection()

    # Sidebar stats and filters
    st.sidebar.header("Filter & Stats")

    # Get date range
    try:
        min_date_str = pd.read_sql_query(
            "SELECT min(sent_date) FROM newsletter", conn
        ).iloc[0, 0]
        max_date_str = pd.read_sql_query(
            "SELECT max(sent_date) FROM newsletter", conn
        ).iloc[0, 0]

        if min_date_str and max_date_str:
            min_date = pd.to_datetime(min_date_str).date()
            max_date = pd.to_datetime(max_date_str).date()

            start_date, end_date = st.sidebar.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )
        else:
            st.sidebar.warning("No data found for date range.")
            start_date, end_date = None, None

        # Stats
        count_newsletters = pd.read_sql_query(
            "SELECT count(*) FROM newsletter", conn
        ).iloc[0, 0]
        count_articles = pd.read_sql_query("SELECT count(*) FROM article", conn).iloc[
            0, 0
        ]

        st.sidebar.markdown(f"**Total Newsletters:** {count_newsletters}")
        st.sidebar.markdown(f"**Total Articles:** {count_articles}")

    except Exception as e:
        st.error(f"Error loading metadata: {e}")
        return

    # Main Search
    search_query = st.text_input("Search Articles", placeholder="Enter search terms...")

    if search_query:
        st.subheader(f"Search Results for '{search_query}'")

        # FTS Query
        query = """
            SELECT 
                a.title, a.text, n.subject, n.sent_date
            FROM article_fts fts
            JOIN article a ON fts.rowid = a.id
            JOIN newsletter n ON a.newsletter_id = n.id
            WHERE article_fts MATCH ?
            ORDER BY n.sent_date DESC
            LIMIT 50
        """
        try:
            results = pd.read_sql_query(query, conn, params=(search_query,))

            if not results.empty:
                for idx, row in results.iterrows():
                    with st.expander(
                        f"{row['title']} | {pd.to_datetime(row['sent_date']).date()} - {row['subject']}"
                    ):
                        st.markdown(row["text"].replace("$", "\\$"))
            else:
                st.info("No results found.")

        except Exception as e:
            st.error(f"Search error: {e}")

    else:
        st.subheader("Latest Newsletters")
        # Show latest newsletters if no search
        query = """
            SELECT id, subject, sent_date FROM newsletter 
            WHERE sent_date BETWEEN ? AND ?
            ORDER BY sent_date DESC LIMIT 10
        """

        # Adjust date filter query parameters
        s_str = start_date.isoformat() if start_date else "1900-01-01"
        e_str = (
            end_date.isoformat() if end_date else "2100-01-01"
        )  # End of day? usually date input is inclusive date

        # Simple string compare works for ISO dates
        results = pd.read_sql_query(query, conn, params=(s_str, e_str))

        for idx, row in results.iterrows():
            st.markdown(f"### {row['subject']}")
            st.caption(f"Date: {pd.to_datetime(row['sent_date']).date()}")

            # Fetch articles for this newsletter
            articles = pd.read_sql_query(
                "SELECT title, text FROM article WHERE newsletter_id = ?",
                conn,
                params=(row["id"],),
            )

            for a_idx, a_row in articles.iterrows():
                with st.expander(a_row["title"]):
                    st.markdown(a_row["text"].replace("$", "\\$"))

            st.divider()

    conn.close()


if __name__ == "__main__":
    main()
