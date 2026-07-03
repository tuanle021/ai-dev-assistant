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