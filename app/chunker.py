import re
from typing import List


def chunk_text(text: str, window_size: int = 3):
    """
    Balanced chunking:
    - preserves context
    - avoids overly large chunks
    - avoids sentence isolation
    """

    import re

    sections = re.split(r'(?=^#{1,6}\s)', text, flags=re.MULTILINE)

    chunks = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.splitlines()
        heading = lines[0] if lines else ""

        body = " ".join(lines[1:])
        sentences = re.split(r'(?<=[.!?])\s+', body)

        sentences = [s.strip() for s in sentences if s.strip()]

        for i in range(0, len(sentences), window_size):
            window = sentences[i:i + window_size]

            chunk = f"{heading}\n{' '.join(window)}"

            chunks.append(chunk)

    return chunks