import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.embedder import embed_text
from app.reranker import rerank
from app.text_processing import tokenize

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

def cosine_similarity(a, b):
    a = np.array(a).flatten()
    b = np.array(b).flatten()

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ---------------------------
# 3. MAIN RETRIEVER
# ---------------------------

def retrieve(query: str, chunks, top_k: int = 3, mode: str = "hybrid"):

    if mode == "keyword":
        return retrieve_keyword(query, chunks, top_k)

    elif mode == "embedding":
        return retrieve_embedding(query, chunks, top_k)

    elif mode == "hybrid":
        # STEP 1: broad candidate generation (IMPORTANT: bigger pool)
        candidates = retrieve_hybrid(query, chunks, top_k=10)

        # STEP 2: rerank candidates
        reranked = rerank(query, candidates, top_k=top_k)

        return reranked
    

def retrieve_keyword(query: str, chunks, top_k: int = 3):

    intent = detect_intent(query)
    query_terms = expand_query(query)

    scored = []

    for chunk in chunks:
        text = chunk["text"].lower()
        score = 0

        for term in query_terms:
            score += text.count(term) * 2

        if query.lower() in text:
            score += 5

        if intent == "process":
            if any(w in text for w in ["flow", "process", "middleware", "routing"]):
                score += 3

        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    # ✅ filter first, then slice
    filtered = [(s, c) for s, c in scored if s > 0]

    return [c for s, c in filtered[:top_k]]

def retrieve_embedding(query: str, chunks, top_k: int = 3):

    query_embedding = embed_text(query)
    scored = []

    for chunk in chunks:
        chunk_embedding = np.array(chunk["embedding"])

        score = cosine_similarity(
            [query_embedding],
            [chunk_embedding]
        )[0][0]

        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [c for s, c in scored[:top_k]]

def retrieve_hybrid(query: str, chunks, top_k: int = 10):

    intent = detect_intent(query)
    query_terms = expand_query(query)
    query_embedding = embed_text(query)

    scored = []

    for chunk in chunks:

        text = chunk["text"].lower()
        lines = chunk["text"].splitlines()
        heading = ""
        if lines: 
            heading = lines[0].lower()

        # ------------------------
        # Semantic score
        # ------------------------
        chunk_embedding = np.array(chunk["embedding"])

        semantic_score = cosine_similarity(
            query_embedding,
            chunk_embedding
        )

        # ------------------------
        # Keyword score
        # ------------------------
        query_tokens = tokenize(query)
        chunk_tokens = tokenize(text)

        common_tokens = query_tokens & chunk_tokens

        keyword_score = len(common_tokens)

        # ------------------------
        # Exact phrase score
        # (Implemented later)
        # ------------------------
        phrase_score = 0

        if query.lower() in text:
            phrase_score = 1

        # ------------------------
        # Heading score
        # (Implemented later)
        # ------------------------
        heading_score = 0

        heading_terms = set(re.findall(r"\w+", heading))
        heading_score = len(set(query_terms) & heading_terms)

        # ------------------------
        # Intent score
        # ------------------------
        intent_score = 0

        if intent == "process":
            if any(w in text for w in ["flow", "process", "middleware", "routing"]):
                intent_score = 1

        elif intent == "definition":
            if any(w in text for w in ["is", "means", "definition"]):
                intent_score = 1

        elif intent == "reason":
            if any(w in text for w in ["because", "reason", "therefore"]):
                intent_score = 1

        # ------------------------
        # Final weighted score
        # ------------------------
        final_score = (
            0.60 * semantic_score +
            0.20 * keyword_score +
            0.10 * heading_score +
            0.05 * phrase_score +
            0.05 * intent_score
        )

        scored.append((final_score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [chunk for score, chunk in scored[:top_k]]