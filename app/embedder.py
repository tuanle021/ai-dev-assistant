from sentence_transformers import SentenceTransformer

# Load model ONCE (important for performance)
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str):
    """
    Convert text into a vector (embedding).
    """
    if not text:
        return []

    embedding = _model.encode(text)

    return embedding.tolist()