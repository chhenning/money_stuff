import os

from money_stuff.db import init_db, populate_db, db_stats
from money_stuff.email_processing import read_emails, process_emails


def main():
    emails_data = read_emails()
    if emails_data:
        newsletters_dict = process_emails(emails_data)

    conn = init_db()
    populate_db(conn, newsletters_dict)
    conn.close()

    db_stats()


if __name__ == "__main__":
    main()
