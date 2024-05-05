# content_filter.py
import re

def load_bad_words(file_path='en.txt'):
    """Load bad words from a file into a set."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return {line.strip().lower() for line in file if line.strip()}

def highlight_text(text, bad_words):
    """Highlight bad words in text with HTML styling."""
    for word in bad_words:
        pattern = re.compile(r'\b(' + re.escape(word) + r')\b', re.IGNORECASE)
        text = pattern.sub(r'<span style="background-color: yellow;">\1</span>', text)
    return text

def filter_text(text, bad_words):
    """Filter bad words from text, replacing them with asterisks."""
    for word in bad_words:
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        text = pattern.sub("*" * len(word), text)
    return text
