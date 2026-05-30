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
    query_terms = query.lower().split()

    scored_chunks = []

    for chunk in chunks:
        text = chunk["text"].lower()

        score = 0

        # 1. Term frequency scoring
        for term in query_terms:
            score += text.count(term)

        # 2. Bonus for exact phrase match
        if query.lower() in text:
            score += 5

        # 3. Normalization (avoid long chunk bias)
        word_count = len(text.split())
        if word_count > 0:
            score = score / word_count * 100

        scored_chunks.append((score, chunk))

    # Sort by best match
    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    # Return top_k chunks
    return [chunk for score, chunk in scored_chunks[:top_k] if score > 0]