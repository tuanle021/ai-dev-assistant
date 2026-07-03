from fastapi import FastAPI
from app.loader import load_text_file
from app.chunker import chunk_text
from app.embedder import embed_text
from app.retriever import save_chunks, load_chunks, retrieve_embedding, retrieve
from app.llm import ask_llm

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Dev Assistant is running"}


@app.post("/ingest")
def ingest():
    """
    Loads sample docs, chunks them, stores them.
    """

    text = load_text_file("data/sample_docs/sample.md")
    chunks = chunk_text(text)

    chunks_with_embeddings = []

    for i, chunk in enumerate(chunks):
        chunks_with_embeddings.append({
            "id": f"chunk_{i}",
            "text": chunk,
            "embedding": embed_text(chunk)
        })

    save_chunks(chunks_with_embeddings)    

    return {"message": "Documents ingested", "chunks": len(chunks)}


@app.post("/ask")
def ask(question: str):
    """
    Ask questions over ingested docs.
    """

    chunks = load_chunks()
    relevant = retrieve(question, chunks, mode="keyword")

    context = "\n\n".join([c["text"] for c in relevant])

    answer = ask_llm(question, context)

    return {
        "question": question,
        "answer": answer,
        "context_used": [c["id"] for c in relevant]
    }