from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.loader import load_text_file
from app.chunker import chunk_text
from app.embedder import embed_text
from app.llm import ask_llm
from app.storage import save_chunks, load_chunks
from app.retrieval_service import RetrievalService
from app.models import QueryRequest
from app.ingestion import ingest_documents

service = None  # global reference (safe pointer)

@asynccontextmanager
async def lifespan(app: FastAPI):

    chunks = load_chunks()

    if not chunks:
        app.state.service = None
        print("⚠️ No chunks found. Please run /ingest first.")
    else:
        app.state.service = RetrievalService(chunks)

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "AI Dev Assistant is running"}


@app.post("/ingest")
def ingest(request: Request):

    chunks = ingest_documents()

    # rebuild runtime service
    request.app.state.service = RetrievalService(chunks)

    return {
        "status": "ingested",
        "chunks": len(chunks)
    }


@app.post("/ask")
def ask(request: Request, payload: QueryRequest):

    service = request.app.state.service

    if service is None:
        return {"error": "No knowledge base found. Please run /ingest first."}

    relevant = service.retrieve(payload.question)

    context = "\n\n".join([c["text"] for c in relevant])

    answer = ask_llm(payload.question, context)

    return {
        "question": payload.question,
        "answer": answer,
        "context_used": [c["id"] for c in relevant]
    }