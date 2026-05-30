import json
from app.retriever import retrieve
from app.storage import load_chunks


# -----------------------------
# Load dataset
# -----------------------------
def load_test_set(path="evaluation/test_set.json"):
    with open(path, "r") as f:
        return json.load(f)


# -----------------------------
# Evaluation logic
# -----------------------------
def evaluate():
    test_set = load_test_set()
    chunks = load_chunks()

    total = len(test_set)
    correct_retrievals = 0

    results = []

    for item in test_set:
        question = item["question"]
        expected = set(item["expected_chunks"])

        retrieved_chunks = retrieve(question, chunks)

        retrieved_ids = set([c["id"] for c in retrieved_chunks])

        match = len(expected.intersection(retrieved_ids)) > 0

        if match:
            correct_retrievals += 1

        results.append({
            "question": question,
            "expected": list(expected),
            "retrieved": list(retrieved_ids),
            "correct": match
        })

        print("\n-----------------------------")
        print("Q:", question)
        print("Expected:", expected)
        print("Retrieved:", retrieved_ids)
        print("Correct:", match)

    accuracy = correct_retrievals / total

    print("\n=============================")
    print(f"Retrieval Accuracy: {accuracy * 100:.2f}%")
    print("=============================")

    return results


if __name__ == "__main__":
    evaluate()