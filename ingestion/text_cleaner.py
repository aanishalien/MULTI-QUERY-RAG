import re

def remove_headers_footer(text, header_patterns=None, footer_patterns=None):
    if header_patterns is None:
        header_patterns = []
    if footer_patterns is None:
        footer_patterns = []

    for pattern in header_patterns + footer_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)

    return text.strip()


def remove_repeated_substrings(text, pattern=r'\.{2,}'):
    text = re.sub(pattern, '.', text).strip()

def remove_extra_spaces(text):
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove multiple newlines
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()

def preprocess_text(text, header_patterns=None, footer_patterns=None):
    text = remove_headers_footer(text, header_patterns, footer_patterns)
    text = remove_repeated_substrings(text)
    text = remove_extra_spaces(text)
    return text

