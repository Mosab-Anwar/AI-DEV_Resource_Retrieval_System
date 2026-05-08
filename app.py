from flask import Flask, jsonify, render_template, request
from search_engine import load_index, rank_query
import json
from pathlib import Path

EVAL_DATA = {}
eval_path = Path("evaluation_data.json")
if eval_path.exists():
    with eval_path.open("r", encoding="utf-8") as f:
        for item in json.load(f):
            EVAL_DATA[item["query"].lower().strip()] = item["relevant_ids"]
app = Flask(__name__)

# Load once at startup
INDEX_DATA = load_index()


@app.get("/")
def home():
    return render_template("search.html")


@app.route("/search", methods=["GET", "POST"])
def search_api():
    if request.method == "GET":
        query = request.args.get("q", "").strip()
        top_k = request.args.get("top_k", default=20, type=int)
    else:
        data = request.get_json(silent=True) or {}
        query = str(data.get("query", "")).strip()
        top_k = int(data.get("top_k", 10))

    if not query:
        return jsonify({"error": "Missing query"}), 400

    results = rank_query(query, INDEX_DATA, top_k=top_k)
    
    for r in results:
        r['is_arxiv'] = 'arxiv.org' in r.get('url', '')
    results.sort(key=lambda x: (not x['is_arxiv'], -x['score']))
    
    return jsonify(
        query=query,
        count=len(results),
        results=results,
    )

@app.get("/results")
def results_page():
    query = request.args.get("q", "").strip()
    top_k = request.args.get("top_k", default=10, type=int)
    if not query:
        return render_template("search.html")
    results = rank_query(query, INDEX_DATA, top_k=top_k)
    relevant_ids = EVAL_DATA.get(query.lower().strip())
    if relevant_ids:
        retrieved_ids = [r["id"] for r in results]
        hits = len(set(relevant_ids) & set(retrieved_ids))
        precision = round(hits / len(retrieved_ids), 3) if retrieved_ids else 0
        recall = round(hits / len(relevant_ids), 3) if relevant_ids else 0
        f1 = round(2 * precision * recall / (precision + recall), 3) if (precision + recall) else 0
        metrics = {"precision": precision, "recall": recall, "f1": f1}
    else:
        metrics = None
    return render_template(
        
        "results.html",
        query=query,
        results=results,
        top_k=top_k,
        metrics=metrics,
    )
if __name__ == "__main__":
    app.run(debug=True)