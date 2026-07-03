import json
from collections import defaultdict
from app.retriever import retrieve
from app.storage import load_chunks


# -----------------------------
# Load dataset
# -----------------------------
def load_test_set(path="evaluation/test_set.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# Metrics helpers
# -----------------------------
def recall_at_k(expected, retrieved_ids):
    return len(set(expected).intersection(retrieved_ids)) > 0


def mrr(expected, retrieved_chunks):
    """
    Mean Reciprocal Rank:
    1 / rank of first relevant result
    """
    expected = set(expected)

    for i, c in enumerate(retrieved_chunks):
        if c["id"] in expected:
            return 1 / (i + 1)

    return 0.0


# -----------------------------
# Evaluation logic
# -----------------------------
def evaluate():
    test_set = load_test_set()
    chunks = load_chunks()

    total = len(test_set)

    recall3_total = 0
    recall5_total = 0
    mrr_total = 0

    by_difficulty = defaultdict(list)
    by_type = defaultdict(list)

    for item in test_set:
        question = item["question"]
        expected = item["expected_chunks"]
        difficulty = item.get("difficulty", "unknown")
        qtype = item.get("type", "unknown")

        # top 3 retrieval
        retrieved_top3 = retrieve(question, chunks, top_k=3)
        retrieved_top5 = retrieve(question, chunks, top_k=5)

        retrieved_ids_3 = [c["id"] for c in retrieved_top3]
        retrieved_ids_5 = [c["id"] for c in retrieved_top5]

        # -------------------------
        # Recall@3
        # -------------------------
        r3 = recall_at_k(expected, retrieved_ids_3)
        recall3_total += int(r3)

        # -------------------------
        # Recall@5
        # -------------------------
        r5 = recall_at_k(expected, retrieved_ids_5)
        recall5_total += int(r5)

        # -------------------------
        # MRR
        # -------------------------
        mrr_score = mrr(expected, retrieved_top3)
        mrr_total += mrr_score

        # -------------------------
        # breakdown tracking
        # -------------------------
        by_difficulty[difficulty].append(int(r3))
        by_type[qtype].append(int(r3))

        # -------------------------
        # debug output per question
        # -------------------------
        print("\n-----------------------------")
        print("Q:", question)
        print("Expected:", expected)
        print("Top3:", retrieved_ids_3)
        print("Recall@3:", r3)

    # -----------------------------
    # Final metrics
    # -----------------------------
    recall_at_3 = recall3_total / total
    recall_at_5 = recall5_total / total
    mean_mrr = mrr_total / total

    print("\n=============================")
    print("OVERALL RESULTS")
    print("=============================")
    print(f"Recall@3: {recall_at_3:.2f}")
    print(f"Recall@5: {recall_at_5:.2f}")
    print(f"MRR: {mean_mrr:.2f}")

    # -----------------------------
    # Breakdown by difficulty
    # -----------------------------
    print("\n=============================")
    print("BY DIFFICULTY")
    print("=============================")

    for k, v in by_difficulty.items():
        print(f"{k}: {sum(v)/len(v):.2f}")

    # -----------------------------
    # Breakdown by type
    # -----------------------------
    print("\n=============================")
    print("BY TYPE")
    print("=============================")

    for k, v in by_type.items():
        print(f"{k}: {sum(v)/len(v):.2f}")


if __name__ == "__main__":
    evaluate()