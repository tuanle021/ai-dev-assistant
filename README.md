# 📌 AI Dev Assistant – RAG System (FastAPI + Hybrid Retrieval + Cross-Encoder Reranking)

## Overview

AI Dev Assistant is a Retrieval-Augmented Generation (RAG) system built with **FastAPI** that allows users to ask questions over technical documentation.

The system combines multiple retrieval strategies to improve context accuracy:

- BM25 lexical retrieval
- Dense vector semantic search
- Hybrid candidate retrieval
- Cross-encoder reranking
- LLM-based answer generation using Groq API

The goal of the project is to build an end-to-end RAG pipeline that focuses on **retrieval quality, evaluation, and production-style architecture**.

---

# 🏗️ Architecture Flow

```text
User Question
      ↓
FastAPI (/ask)
      ↓
Retrieval Service
      |
      ├── BM25 Retriever
      |       |
      |       └── Keyword-based matching
      |
      ├── Semantic Retriever
      |       |
      |       └── Embedding similarity search
      |
      ↓
Candidate Fusion
      ↓
CrossEncoder Reranker
      ↓
Top-K Relevant Chunks
      ↓
LLM (Groq / Llama 3.1)
      ↓
Generated Answer
```

---

# ⚙️ Core Components

## 1. Document Chunking System

The ingestion pipeline converts documentation into searchable chunks.

Features:

- Splits Markdown documents by headings
- Preserves document structure and context
- Creates smaller retrieval units for improved relevance

Example:

```text
FastAPI Documentation

        ↓

chunk_0
chunk_1
chunk_2
...
```

---

# 2. Storage Layer

Processed chunks are stored in:

```
storage/chunks.json
```

Each chunk contains:

```json
{
  "id": "chunk_0",
  "text": "FastAPI is a modern Python framework...",
  "embedding": [
      0.123,
      0.456,
      ...
  ]
}
```

Stored fields:

- `id`
- `text`
- `embedding vector`

Embeddings are generated using HuggingFace sentence-transformer models.

---

# 3. Retrieval System

The retrieval layer uses a hybrid search architecture combining lexical and semantic retrieval.

The purpose is to improve recall by finding relevant information using different signals.

---

## 🔹 BM25 Lexical Retrieval

Uses:

```
BM25Okapi
```

Features:

- Keyword-based matching
- Strong performance for exact terminology
- Heading boosting to improve section retrieval

Example:

Query:

```
What is dependency injection in FastAPI?
```

BM25 identifies chunks containing:

```
dependency
Depends
injection
```

---

## 🔹 Semantic Retrieval

Uses:

- HuggingFace sentence-transformer embeddings
- Vector similarity search
- Cosine similarity scoring

Instead of matching exact words, semantic retrieval identifies similar meanings.

Example:

Query:

```
Why does FastAPI use async?
```

Can retrieve:

```
Asynchronous execution improves request handling performance
```

even without identical keywords.

---

## 🔹 Hybrid Retrieval Pipeline

The system combines both retrieval approaches:

```text
              User Query

                  ↓

        +-------------------+
        |                   |
        ↓                   ↓

      BM25            Semantic Search

        |                   |

        +---------+---------+

                  ↓

          Candidate Pool

                  ↓

          CrossEncoder Reranker

                  ↓

             Top-K Chunks
```

Benefits:

- BM25 improves precision for exact terms
- Semantic search improves conceptual matching
- Combined retrieval improves overall recall

---

# 4. Reranking Layer

Retrieved candidates are passed through a CrossEncoder reranking model:

```
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Unlike embedding similarity, the CrossEncoder evaluates:

```
(query, document)
```

pairs directly.

Example:

```
(
 "What is Pydantic used for?",
 "FastAPI uses Pydantic models for request validation"
)
```

The model produces a relevance score and sorts candidates based on query-document relevance.

Benefits:

- Improves ranking precision
- Removes weaker candidates
- Prioritises the most useful context for generation

---

# 5. Evaluation System

The project includes a custom retrieval evaluation framework inspired by RAG evaluation approaches.

The evaluation framework measures retrieval quality before generating answers.

---

## Metrics

### Recall@K

Measures whether the correct chunk appears within the top K retrieved results.

Example:

```
Expected:
chunk_4

Retrieved:
chunk_4
chunk_2
chunk_7
```

Recall@3 = True

---

### MRR (Mean Reciprocal Rank)

Measures how highly the correct document is ranked.

A higher score means relevant chunks appear closer to the top.

---

## Evaluation Breakdown

Results are analysed by:

### Difficulty

- Easy
- Medium
- Hard


### Question Type

- Factual
- Conceptual
- Reasoning
- Procedural
- Multi-hop

---

# 📊 Current Performance

Latest retrieval evaluation:

| Metric | Score |
|---|---:|
| Recall@3 | 1.00 |
| Recall@5 | 1.00 |
| MRR | 0.72 |

Breakdown:

| Category | Score |
|---|---:|
| Easy | 1.00 |
| Medium | 1.00 |
| Hard | 1.00 |
| Factual | 1.00 |
| Conceptual | 1.00 |
| Reasoning | 1.00 |
| Procedural | 1.00 |
| Multi-hop | 1.00 |

---

# 🧠 Key Engineering Decisions

## Hybrid Retrieval

Selected because different query types require different retrieval signals:

- Exact terminology → BM25
- Conceptual questions → embeddings
- Final precision → reranking

---

## CrossEncoder Reranking

Implemented as a second-stage retrieval layer because:

- Vector similarity alone can return semantically similar but incorrect chunks
- Reranking improves ordering before passing context to the LLM

---

## Structure-Aware Chunking

Markdown headings are preserved because:

- Documentation structure contains useful context
- Section titles improve retrieval accuracy
- Smaller chunks reduce irrelevant context

---

# 🚧 Current Limitations

Although retrieval performance is currently strong, future improvements include:

- Larger evaluation dataset
- Hard negative examples
- Retrieval benchmarking against larger document collections
- Hybrid retrieval weight tuning
- Metadata filtering
- Vector database integration

---

# 🔜 Future Roadmap

## Priority 1

Improve evaluation depth:

- Increase dataset size
- Add more difficult questions
- Add retrieval comparison reports


## Priority 2

Production improvements:

- Add vector database support
- Add caching layer
- Add document metadata filtering
- Add conversation memory


## Priority 3

Advanced RAG improvements:

- Query rewriting
- Multi-query retrieval
- Context compression
- Agent-based retrieval workflows

---

# 🚀 Demo

## Ask a Question

Send a request to:

```
POST /ask
```

Example:

```json
{
  "question": "What is dependency injection in FastAPI?"
}
```

Response:

```json
{
  "question": "What is dependency injection in FastAPI?",
  "answer": "Dependency injection allows reusable components to be automatically provided to API routes using FastAPI's Depends system.",
  "context_used": [
    "chunk_2",
    "chunk_6",
    "chunk_3"
  ]
}
```

---

# ⚙️ API Endpoints

## 1. Health Check

```
GET /
```

Response:

```json
{
  "message": "AI Dev Assistant is running"
}
```

---

## 2. Ingest Documents

```
POST /ingest
```

This endpoint:

- Loads documentation
- Splits documents into chunks
- Generates embeddings
- Stores processed chunks

Example response:

```json
{
  "message": "Documents ingested",
  "chunks": 12
}
```

---

## 3. Ask Question

```
POST /ask
```

Request:

```json
{
  "question": "How does FastAPI handle async operations?"
}
```

Response:

```json
{
  "question": "How does FastAPI handle async operations?",
  "answer": "FastAPI supports asynchronous programming using async and await.",
  "context_used": [
    "chunk_3",
    "chunk_8"
  ]
}
```

---

# 🧠 RAG Execution Flow

When a user sends a question:

1. FastAPI receives the request through `/ask`
2. Query is sent to the Retrieval Service
3. BM25 retrieves keyword-matching chunks
4. Semantic search retrieves similar chunks using embeddings
5. Results are merged into a candidate pool
6. CrossEncoder reranks candidates
7. Top-K chunks are provided to the LLM
8. LLM generates the final response

---

# 🛠️ Tech Stack

Backend:

- Python
- FastAPI

Retrieval:

- rank-bm25
- Sentence Transformers
- HuggingFace embeddings

AI:

- Groq API
- Llama 3.1

Storage:

- JSON document storage

Evaluation:

- Custom RAG retrieval evaluation framework
- Recall@K
- MRR