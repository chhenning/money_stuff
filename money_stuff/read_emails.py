import mailbox
import os
import json
import email.utils
from datetime import datetime, timezone
from email.header import decode_header


def extract_html(msg):
    """
    Extracts the HTML body from the email message.
    """
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/html" and "attachment" not in content_disposition:
                try:
                    return part.get_payload(decode=True).decode()
                except Exception as e:
                    print(f"Error decoding HTML part: {e}")
                    continue
    else:
        # If not multipart, check if the single part is HTML
        if msg.get_content_type() == "text/html":
            try:
                return msg.get_payload(decode=True).decode()
            except Exception as e:
                print(f"Error decoding HTML body: {e}")

    return None


def parse_date(date_str):
    """
    Parses the email date string into a UTC timestamp.
    """
    if not date_str:
        return None
    try:
        parsed_date = email.utils.parsedate_to_datetime(date_str)
        # Convert to UTC
        utc_date = parsed_date.astimezone(timezone.utc)
        return utc_date.isoformat()
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return None


def decode_subject(header_value):
    if not header_value:
        return ""
    decoded_list = decode_header(header_value)
    subject_parts = []
    for content, encoding in decoded_list:
        if isinstance(content, bytes):
            if encoding:
                subject_parts.append(content.decode(encoding, errors="ignore"))
            else:
                # Default to utf-8 if encoding is unknown or None
                subject_parts.append(content.decode("utf-8", errors="ignore"))
        else:
            subject_parts.append(str(content))
    return "".join(subject_parts)


def main():
    mbox_file = "data/Money Stuff.mbox"
    output_file = "data/emails.json"

    if not os.path.exists(mbox_file):
        print(f"Error: File not found at {mbox_file}")
        return

    print(f"Opening {mbox_file}...")

    try:
        mbox = mailbox.mbox(mbox_file)
        print(f"Successfully opened mbox.")

        emails_data = []
        count = 0

        for message in mbox:
            count += 1
            subject = decode_subject(message["subject"])
            date_str = message["date"]
            timestamp = parse_date(date_str)
            html_content = extract_html(message)

            if html_content:
                emails_data.append(
                    {
                        "subject": subject,
                        "timestamp": timestamp,
                        "content": html_content,
                    }
                )

            if count % 100 == 0:
                print(f"Processed {count} emails...")

        print(f"\nTotal emails processed: {count}")
        print(f"Extracted {len(emails_data)} emails with HTML content.")

        print(f"Saving to {output_file}...")
        with open(output_file, "w") as f:
            json.dump(emails_data, f, indent=4)
        print("Done.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
