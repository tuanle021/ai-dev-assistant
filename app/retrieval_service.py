from app.bm25 import BM25Retriever
from app.semantic_search import SemanticRetriever
from app.reranker import rerank
from app.tokenizer import tokenize


class RetrievalService:

    def __init__(self, chunks):

        self.chunks = chunks

        self.bm25 = BM25Retriever(chunks)
        self.semantic = SemanticRetriever(chunks)


    def retrieve(self, query: str, top_k: int = 3):

        lexical_results = self.bm25.retrieve(
            query,
            top_k=10
        )

        semantic_results = self.semantic.retrieve(
            query,
            top_k=10
        )


        print("\nQUERY:", query)

        print(
            "BM25:",
            [c["id"] for c in lexical_results]
        )

        print(
            "SEMANTIC:",
            [c["id"] for c in semantic_results]
        )

        candidates = {
            c["id"]: c
            for c in lexical_results + semantic_results
        }


        candidates = list(candidates.values())

        reranked_results = rerank(
            query,
            candidates,
            top_k=len(candidates)
        )

        print(
            "FULL RERANK:",
            [
                (
                 c["id"],
                round(c["rerank_score"], 3)
                )
                for c in reranked_results
            ]
        )

        return reranked_results
    