import json

CHUNKS_FILE = "storage/chunks.json"


def load_chunks(path: str = CHUNKS_FILE):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_chunks(chunks, path: str = CHUNKS_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)