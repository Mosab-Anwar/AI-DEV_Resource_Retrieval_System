import json
from collections import Counter
from pathlib import Path
from preprocessing import preprocess

CORPUS_FILE = Path("corpus.json")
INDEX_FILE = Path("index.json")

def load_corpus(path=CORPUS_FILE):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def build_index(corpus):
    inverted_index = {}
    documents = {}
    total_doc_length = 0
    for doc in corpus:
        doc_id = str(doc.get("id", "")).strip()
        if not doc_id:
            continue
        text = str(doc.get("text", ""))
        tokens = preprocess(text)
        tf = Counter(tokens)
        total_doc_length += len(tokens)
        documents[doc_id] = {
            "title": doc.get("title", ""),
            "source": doc.get("source", ""),
            "url": doc.get("url", ""),
            "text": doc.get("text", "")[:2000],
        }
        for term, freq in tf.items():
            if term not in inverted_index:
                inverted_index[term] = {"df": 0, "postings": {}}
            inverted_index[term]["postings"][doc_id] = freq
    for term in inverted_index:
        inverted_index[term]["df"] = len(inverted_index[term]["postings"])
    num_documents = len(documents)
    return {
        "index": inverted_index,
        "documents": documents,
        "num_documents": num_documents,
        "avg_doc_length": total_doc_length / num_documents if num_documents else 0,
    }

def main():
    corpus = load_corpus()
    index_data = build_index(corpus)
    with INDEX_FILE.open("w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    print(f"Documents: {index_data['num_documents']}")

if __name__ == "__main__":
    main()