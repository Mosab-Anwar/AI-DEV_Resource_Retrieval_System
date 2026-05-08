import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from preprocessing import preprocess

import nltk
from markupsafe import Markup, escape

INDEX_FILE = Path("index.json")
TOP_K = 10


def load_index(path: Path = INDEX_FILE) -> dict:
    if not path.exists():
        raise FileNotFoundError("index.json not found. Run index_builder.py first.")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _make_snippet(meta: dict, query: str, max_chars: int = 260) -> Markup:
    """
    Build a short snippet from available document text and highlight query words.
    Looks for common text keys so it works with different corpus formats.
    """
    raw_text = (
        meta.get("text")
        or meta.get("content")
        or meta.get("snippet")
        or meta.get("abstract")
        or meta.get("description")
        or ""
    )

    text = str(raw_text).strip()
    if not text:
        return Markup("")

    query_words = sorted(set(re.findall(r"[A-Za-z]+", query.lower())), key=len, reverse=True)
    if not query_words:
        short = escape(text[:max_chars])
        return Markup(str(short) + ("..." if len(text) > max_chars else ""))

    lower_text = text.lower()
    hit_positions = [lower_text.find(w) for w in query_words if lower_text.find(w) != -1]

    if hit_positions:
        start = max(0, min(hit_positions) - 60)
    else:
        start = 0

    end = min(len(text), start + max_chars)
    snippet = text[start:end]
    safe = str(escape(snippet))

    for word in query_words:
        safe = re.sub(rf"(?i)\b({re.escape(word)})\b", r"<mark>\1</mark>", safe)

    if start > 0:
        safe = "… " + safe
    if end < len(text):
        safe = safe + " …"

    return Markup(safe)


def rank_query(query: str, index_data: dict, top_k: int = TOP_K) -> list[dict]:
    """
    Simple TF-IDF ranking:
    score(doc, query) = sum((tf_q * idf) * (tf_d * idf))
    """
    query_terms = preprocess(query)
    if not query_terms:
        return []

    query_tf = Counter(query_terms)
    index = index_data["index"]
    documents = index_data["documents"]
    num_docs = index_data["num_documents"]

    scores = defaultdict(float)

    for term, q_tf in query_tf.items():
        term_data = index.get(term)
        if not term_data:
            continue

        df = term_data["df"]
        if df == 0:
            continue

        idf = math.log(num_docs / df) + 1
        q_weight = q_tf * idf

        for doc_id, d_tf in term_data["postings"].items():
            d_weight = d_tf * idf
            scores[doc_id] += q_weight * d_weight

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]

    results = []
    for doc_id, score in ranked:
        meta = documents.get(doc_id, {})
        results.append({
            "id": doc_id,
            "score": round(score, 6),
            "type": meta.get("type", meta.get("source_type", "")),
            "title": meta.get("title", ""),
            "source": meta.get("source", ""),
            "url": meta.get("url", ""),
            "snippet": _make_snippet(meta, query),
        })

    return results