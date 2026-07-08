from rank_bm25 import BM25Okapi
from app.tokenizer import tokenize

class BM25Retriever:

    def __init__(self, chunks):

        if not chunks:
            self.index = None
            self.chunks = []
            return

        self.chunks = chunks
        corpus = []

        for c in chunks:

            text = c["text"]

            lines = text.splitlines()

            heading = lines[0] if lines else ""

            boosted_text = (
                heading + " "
                + heading + " "
                + text
            )

            corpus.append(
                list(tokenize(boosted_text))
            )

        self.index = BM25Okapi(corpus)

    def retrieve(self, query: str, top_k: int = 5):

        if self.index is None:
            return []

        tokenized_query = list(tokenize(query))

        scores = self.index.get_scores(tokenized_query)

        ranked = sorted(
         zip(scores, self.chunks),
            key=lambda x: x[0],
            reverse=True
        )

        return [c for _, c in ranked[:top_k]]