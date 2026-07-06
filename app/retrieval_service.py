from app.bm25 import BM25Retriever
from app.semantic_search import SemanticRetriever
from app.reranker import rerank


class RetrievalService:

    def __init__(self, chunks):
        self.chunks = chunks

        # build ONCE
        self.bm25 = BM25Retriever(chunks)
        self.semantic = SemanticRetriever(chunks)

    def retrieve(self, query: str, top_k: int = 3):

        # Step 1: candidate generation
        lexical_results = self.bm25.retrieve(query, top_k=20)
        semantic_results = self.semantic.retrieve(query, top_k=20)

        # Step 2: merge + deduplicate
        candidates = {c["id"]: c for c in lexical_results + semantic_results}
        candidates = list(candidates.values())

        # Step 3: rerank
        return rerank(query, candidates, top_k=top_k)