📌 AI Dev Assistant – RAG System (FastAPI + Hybrid Retrieval + Reranking)
Overview

This project is a Retrieval-Augmented Generation (RAG) system built with FastAPI, designed to answer questions over technical documentation using a combination of:

Keyword-based retrieval
Dense vector (embedding) search
Hybrid retrieval strategy
Cross-encoder reranking
LLM-based answer generation (Groq API)

🏗️ Architecture
User Question
    ↓
FastAPI (/ask)
    ↓
Retriever (Hybrid Mode)
    ├── Keyword Retrieval (lexical match)
    ├── Embedding Retrieval (semantic search)
    └── Candidate Fusion
            ↓
Reranker (Cross-Encoder)
    ↓
Top-K Relevant Chunks
    ↓
LLM (Groq / Llama 3.1)
    ↓
Final Answer

⚙️ Core Components
1. Chunking System
Splits Markdown documents by headings
Preserves semantic structure for better retrieval
2. Storage Layer
Chunks stored as JSON (storage/chunks.json)
Each chunk includes:
id
text
embedding vector
3. Retrieval System

Supports 3 retrieval modes:

🔹 Keyword Retrieval
TF-style scoring
Synonym expansion
Intent detection (what / how / why)
🔹 Embedding Retrieval
Uses HuggingFace sentence embeddings
Cosine similarity search
🔹 Hybrid Retrieval (Recommended)
Combines keyword + embedding signals
Produces candidate pool
Feeds reranker for final ordering
4. Reranking Layer
Cross-encoder model reranks top candidates
Improves precision significantly (MRR boost observed)
5. Evaluation System

Custom evaluation suite inspired by RAGAS-lite:

Metrics:

Recall@K
MRR (Mean Reciprocal Rank)
Breakdown by:
difficulty (easy / medium / hard)
question type (factual / conceptual / reasoning / procedural / multi-hop)

📊 Current Performance
Recall@3: 0.62
Recall@5: 0.77
MRR: 0.55
Insights:
Strong performance on conceptual & reasoning questions
Weakness in factual retrieval (keyword precision gap)
Reranking significantly improved ranking quality

🧠 Key Design Decisions
Hybrid retrieval chosen over pure embeddings for robustness
Reranking used to improve precision after candidate generation
Chunking based on document structure (Markdown headings)
Intent detection used to bias scoring

🚧 Current Limitations
Factual retrieval still under-optimized
Chunk granularity not fully tuned
Hybrid scoring weights need refinement (Priority 3)

🔜 Next Improvements (Roadmap)
Improve hybrid scoring balance (Priority 3)
Add better lexical anchoring for factual queries
Optimize chunking strategy for precision
Improve evaluation dataset further (hard negatives)