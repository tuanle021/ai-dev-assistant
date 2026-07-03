from sentence_transformers import CrossEncoder

# lightweight but strong reranker model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query: str, chunks, top_k: int = 3):
    """
    Re-ranks retrieved chunks using a cross-encoder model.
    """

    if not chunks:
        return []

    pairs = [(query, chunk["text"]) for chunk in chunks]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(scores, chunks),
        key=lambda x: x[0],
        reverse=True
    )

    return [chunk for _, chunk in ranked[:top_k]]