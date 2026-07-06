import numpy as np
from app.embedder import embed_text

def cosine_similarity(a, b):
    a = np.array(a).flatten()
    b = np.array(b).flatten()

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

class SemanticRetriever:

    def __init__(self, chunks):
        self.chunks = chunks

    def retrieve(self, query, top_k=10):

        query_embedding = embed_text(query)

        scored = []

        for chunk in self.chunks:

            score = cosine_similarity(
                query_embedding,
                np.array(chunk["embedding"])
            )

            scored.append((score, chunk))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [chunk for score, chunk in scored[:top_k]]