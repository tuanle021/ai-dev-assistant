import re

def chunk_text(text: str):
    """
    Split markdown documents by headings.

    Each heading section becomes a chunk.
    """

    sections = re.split(r'(?=^#{1,6}\s)', text, flags=re.MULTILINE)

    chunks = []

    for section in sections:
        section = section.strip()

        if section:
            chunks.append(section)

    return chunks