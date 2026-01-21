import re


def clean_markdown_for_ml(text: str) -> str:
    # Replace markdown links [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove bare URLs
    text = re.sub(r"https?://\S+", "", text)

    # Optional: collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
