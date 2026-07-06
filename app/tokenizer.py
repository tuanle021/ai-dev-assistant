import re

STOPWORDS = {
    "what",
    "how",
    "why",
    "is",
    "are",
    "the",
    "a",
    "an",
    "of",
    "to",
    "for",
    "in",
    "on",
    "does",
    "do",
    "when",
    "can",
    "with"
}

def tokenize(text: str):
    """
    Lowercase, remove punctuation and stopwords.
    Returns a set of meaningful words.
    """

    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

    return {
        word
        for word in words
        if word not in STOPWORDS
    }