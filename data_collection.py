import json
import os
import time

from github import Auth, Github
from arxiv import Client, Search, SortCriterion

queries = ["machine learning", "deep learning", "artificial intelligence"]
corpus = []
seen = set()
doc_id = 1

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise SystemExit("Please set GITHUB_TOKEN first.")

g = Github(auth=Auth.Token(token))

print("Collecting GitHub repos...")
for query in queries:
    count = 0
    for repo in g.search_repositories(query=query, sort="stars", order="desc"):
        if count >= 1500:
            break

        if repo.full_name in seen:
            continue
        seen.add(repo.full_name)

        try:
            readme = repo.get_readme().decoded_content.decode("utf-8", errors="ignore")
        except Exception:
            readme = ""

        try:
            topics = repo.get_topics()
        except Exception:
            topics = []

        corpus.append({
            "id": f"gh_{doc_id}",
            "source": "github",
            "title": repo.full_name,
            "text": f"{repo.description or ''} {readme[:3000]}",
            "url": repo.html_url,
            "topics": topics
        })

        doc_id += 1
        count += 1
        time.sleep(0.15)

print("Collecting arXiv papers...")
client = Client(page_size=100, delay_seconds=3.0, num_retries=3)
search = Search(
    query='("machine learning" OR "deep learning" OR "artificial intelligence")',
    max_results=500,
    sort_by=SortCriterion.SubmittedDate
)

for paper in client.results(search):
    corpus.append({
        "id": f"ax_{doc_id}",
        "source": "arxiv",
        "title": paper.title,
        "text": paper.summary,
        "url": paper.entry_id
    })
    doc_id += 1

with open("corpus.json", "w", encoding="utf-8") as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"Saved {len(corpus)} documents.")