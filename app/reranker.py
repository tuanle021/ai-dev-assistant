from sentence_transformers import CrossEncoder
from app.tokenizer import tokenize


# semantic reranker
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def calculate_lexical_score(query, chunk):
    """
    Calculates keyword overlap between query and chunk.
    """

    query_tokens = set(tokenize(query))
    chunk_tokens = set(tokenize(chunk["text"]))

    if not query_tokens:
        return 0

    overlap = query_tokens.intersection(chunk_tokens)

    return len(overlap) / len(query_tokens)



def rerank(query: str, chunks, top_k: int = 3):
    """
    Hybrid reranking:
    
    1. Cross encoder semantic score
    2. Lexical keyword score
    """

    if not chunks:
        return []


    pairs = [
        (query, chunk["text"])
        for chunk in chunks
    ]


    semantic_scores = reranker.predict(pairs)


    ranked_chunks = []


    for chunk, semantic_score in zip(
        chunks,
        semantic_scores
    ):

        lexical_score = calculate_lexical_score(
            query,
            chunk
        )


        # Hybrid scoring
        final_score = (
            semantic_score * 0.7
            +
            lexical_score * 0.3
        )


        ranked_chunks.append(
            (
                final_score,
                chunk
            )
        )


    ranked = sorted(
        ranked_chunks,
        key=lambda x: x[0],
        reverse=True
    )


    return [
      {
          **chunk,
          "rerank_score": float(score)
      }
      for score, chunk in ranked[:top_k]
    ]