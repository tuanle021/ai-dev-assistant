import json
import re

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


# ---------------------------
# 1. SIMPLE INTENT DETECTION
# ---------------------------
def detect_intent(query: str):
    q = query.lower()

    if "how" in q:
        return "process"
    if "why" in q:
        return "reason"
    if "what" in q:
        return "definition"

    return "general"


# ---------------------------
# 2. SYNONYM EXPANSION MAP
# ---------------------------
SYNONYMS = {
    "lifecycle": ["flow", "process", "request", "handling", "execution", "middleware"],
    "authentication": ["auth", "security", "jwt", "login"],
    "dependency": ["injection", "depends", "ioc"],
    "async": ["asynchronous", "await", "concurrent"],
}


def expand_query(query: str):
    terms = query.lower().split()
    expanded = set(terms)

    for term in terms:
        if term in SYNONYMS:
            expanded.update(SYNONYMS[term])

    return list(expanded)


# ---------------------------
# 3. MAIN RETRIEVER
# ---------------------------
def retrieve(query: str, chunks, top_k: int = 3):

    intent = detect_intent(query)
    query_terms = expand_query(query)

    scored_chunks = []

    for chunk in chunks:
        text = chunk["text"].lower()
        score = 0

        # 1. keyword + synonym match
        for term in query_terms:
            score += text.count(term) * 2

        # 2. phrase match boost
        if query.lower() in text:
            score += 5

        # 3. heading boost (VERY IMPORTANT)
        if re.search(r"^#+\s.*", chunk["text"], re.MULTILINE):
            score += 3

        # 4. intent alignment boost
        if intent == "process":
            if any(word in text for word in ["flow", "process", "request", "middleware", "routing"]):
                score += 4

        elif intent == "definition":
            if any(word in text for word in ["is", "definition", "means", "refers"]):
                score += 3

        elif intent == "reason":
            if any(word in text for word in ["because", "therefore", "why", "reason"]):
                score += 3

        # 5. normalization
        word_count = len(text.split())
        if word_count > 0:
            score = score / word_count * 100

        scored_chunks.append((score, chunk))

    # sort best first
    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    return [chunk for score, chunk in scored_chunks[:top_k] if score > 0]