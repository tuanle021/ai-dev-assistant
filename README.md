# 📌 AI Dev Assistant – RAG System (FastAPI + Hybrid Retrieval + Reranking)

## Overview

This project is a Retrieval-Augmented Generation (RAG) system built with **FastAPI**, designed to answer questions over technical documentation using a combination of:

- Keyword-based retrieval
- Dense vector (embedding) search
- Hybrid retrieval strategy
- Cross-encoder reranking
- LLM-based answer generation (Groq API)

---

## 🏗️ Architecture Flow

```text
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
```
---

## ⚙️ Core Components

### 1. Chunking System
- Splits Markdown documents by headings
- Preserves semantic structure for better retrieval quality

---

### 2. Storage Layer
- Chunks stored in JSON format: `storage/chunks.json`
- Each chunk contains:
  - `id`
  - `text`
  - `embedding` vector

---

### 3. Retrieval System

The system supports three retrieval modes:

#### 🔹 Keyword Retrieval
- TF-style scoring
- Synonym expansion
- Intent detection (what / how / why queries)

#### 🔹 Embedding Retrieval
- Uses HuggingFace sentence-transformer embeddings
- Cosine similarity for semantic search

#### 🔹 Hybrid Retrieval (Recommended)
- Combines keyword + embedding signals
- Generates candidate pool
- Sends results to reranker for final ranking

---

### 4. Reranking Layer
- Cross-encoder model reranks retrieved candidates
- Significantly improves ranking quality (observed MRR improvement)

---

### 5. Evaluation System

Custom evaluation framework inspired by RAGAS-lite.

#### Metrics:
- Recall@K
- MRR (Mean Reciprocal Rank)

#### Breakdown analysis:
- Difficulty levels:
  - Easy
  - Medium
  - Hard

- Question types:
  - Factual
  - Conceptual
  - Reasoning
  - Procedural
  - Multi-hop

---

## 📊 Current Performance

| Metric     | Score |
|------------|-------|
| Recall@3   | 0.62  |
| Recall@5   | 0.77  |
| MRR        | 0.55  |

### Insights
- Strong performance on conceptual and reasoning queries
- Weak performance on factual retrieval (keyword precision gap)
- Reranking significantly improved ranking quality

---

## 🧠 Key Design Decisions

- Hybrid retrieval chosen for robustness across query types
- Reranking improves precision after candidate generation
- Chunking based on Markdown structure (headings)
- Intent detection used to bias keyword scoring

---

## 🚧 Current Limitations

- Factual retrieval still under-optimized
- Chunk granularity not fully tuned
- Hybrid scoring weights require further calibration (Priority 3)

---

## 🔜 Next Improvements (Roadmap)

- Improve hybrid scoring balance (Priority 3)
- Strengthen lexical matching for factual queries
- Optimize chunking strategy for precision
- Expand evaluation dataset with harder negatives

## 🚀 Demo

### Ask a Question

Send a request to the `/ask` endpoint with a question about the ingested documentation.

Example:

```bash
POST /ask
Content-Type: application/json

{
  "question": "What is dependency injection in FastAPI?"
}
```

```bash
{
  "question": "What is dependency injection in FastAPI?",
  "answer": "Dependency injection in FastAPI is a design pattern that allows components to be loosely coupled. It is implemented using the Depends system, where dependencies are automatically resolved and injected into path operations.",
  "context_used": [
    "chunk_2",
    "chunk_6",
    "chunk_3"
  ]
}
```

## ⚙️ API Endpoints
### 1. Health Check
```bash
GET /
```
#### Response

```json
{
  "message": "AI Dev Assistant is running"
}
```
### 2. Ingest Documents
```bash
POST /ingest
```
This endpoint:

- Loads source documentation
- Splits it into chunks
- Stores chunks with embeddings

#### Response

```json
{
  "message": "Documents ingested",
  "chunks": 12
}
```
### 3. Ask a Question (RAG Pipeline)
```bash
POST /ask
```
#### Request Body
```json
{
  "question": "How does FastAPI handle async operations?"
}
```

#### Response
```json
{
  "question": "How does FastAPI handle async operations?",
  "answer": "FastAPI supports asynchronous programming using async and await, allowing non-blocking I/O and concurrent request handling for improved performance.",
  "context_used": [
    "chunk_5",
    "chunk_3",
    "chunk_7"
  ]
}
```

## 🧠 What Happens Behind the API Call
1. Question is received via /ask
2. Retriever selects relevant chunks using:
    - keyword scoring
    - embedding similarity
    - hybrid fusion
3. Cross-encoder reranks candidates
4. Top-K chunks are passed to the LLM
5. LLM generates final answer