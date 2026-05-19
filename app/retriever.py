import json

def save_chunks(chunks, path="storage/chunks.json"):
    data = []

    for i, chunk in enumerate(chunks):
        data.append({
            "id": f"chunk_{i}",
            "text": chunk
        })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_chunks(path="storage/chunks.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve(query: str, chunks, top_k: int = 3):
    """
    Very simple keyword scoring retriever.
    """

    scored = []

    for chunk in chunks:
        score = 0

        for word in query.lower().split():
            if word in chunk["text"].lower():
                score += 1

        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [c[1] for c in scored[:top_k]]