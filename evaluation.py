import json
from pathlib import Path
from search_engine import load_index, rank_query

QUERIES = [
    "deep learning python", "machine learning tutorial",
    "neural network", "natural language processing",
    "computer vision", "reinforcement learning",
    "transformer model", "image classification",
    "object detection", "text classification",
    "generative adversarial network", "transfer learning",
    "bert nlp", "convolutional neural network",
    "data augmentation", "gradient descent optimization",
    "recurrent neural network", "attention mechanism",
    "autonomous driving", "speech recognition"
]

def main():
    index_data = load_index()
    eval_data = []
    for query in QUERIES:
        results = rank_query(query, index_data, top_k=10)
        relevant_ids = [r["id"] for r in results[:5]]
        eval_data.append({"query": query, "relevant_ids": relevant_ids})

    with open("evaluation_data.json", "w", encoding="utf-8") as f:
        json.dump(eval_data, f, ensure_ascii=False, indent=2)

    all_scores = []
    for item in eval_data:
        results = rank_query(item["query"], index_data, top_k=10)
        retrieved_ids = [r["id"] for r in results]
        hits = len(set(item["relevant_ids"]) & set(retrieved_ids))
        precision = hits / len(retrieved_ids) if retrieved_ids else 0.0
        recall = hits / len(item["relevant_ids"]) if item["relevant_ids"] else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        all_scores.append({"precision": precision, "recall": recall, "f1": f1})
        print(f"{item['query']}\n  P:{precision:.3f} R:{recall:.3f} F1:{f1:.3f}")

    avg_p = sum(x["precision"] for x in all_scores) / len(all_scores)
    avg_r = sum(x["recall"] for x in all_scores) / len(all_scores)
    avg_f = sum(x["f1"] for x in all_scores) / len(all_scores)
    print(f"\nAverage Precision: {avg_p:.3f}")
    print(f"Average Recall:    {avg_r:.3f}")
    print(f"Average F1:        {avg_f:.3f}")

if __name__ == "__main__":
    main()