import os
from app.storage import save_chunks
from app.chunker import chunk_text
from app.embedder import embed_text


def ingest_documents(doc_path: str = "data/sample_docs"):

    chunks = []

    for filename in os.listdir(doc_path):

        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(doc_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        split_chunks = chunk_text(text)

        for chunk in split_chunks:

            embedding = embed_text(chunk)

            chunks.append({
                "id": f"chunk_{len(chunks)}",
                "text": chunk,
                "embedding": embedding
            })

    save_chunks(chunks)

    return chunks