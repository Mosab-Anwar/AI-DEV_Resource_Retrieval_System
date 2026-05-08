# AI-DEV_Resource_Retrieval_System

A full Information Retrieval (IR) system that allows users to search across
GitHub repositories and arXiv research papers in the field of AI and Machine Learning.
Built from scratch using Python — no external search engines involved.

---

## What It Does

You type a query like `deep learning python` and the system searches through
a locally stored corpus of 3,000+ documents (GitHub READMEs + arXiv abstracts),
ranks them by relevance using TF-IDF scoring, and returns the most relevant
results with highlighted snippets and direct links to the original source.

---

## How It Works

The system is built around a classic IR pipeline:

1. **Data Collection** — GitHub API and arXiv API are used once to collect
   1,500+ repositories and 500+ research papers, stored locally in `corpus.json`

2. **Preprocessing** — Each document goes through tokenization, lowercasing,
   stop word removal, and Porter stemming using NLTK

3. **Inverted Index** — A term-based index is built from the corpus and stored
   in `index.json`, mapping each word to the documents it appears in

4. **TF-IDF Ranking** — At search time, the query is preprocessed and scored
   against the index using TF-IDF weighting

5. **Web Interface** — A lightweight Flask app serves the search interface
   with highlighted snippets and relevance scores

6. **Evaluation** — The system is evaluated on 20 test queries using
   Precision, Recall, and F1 Score

---

## Tech Stack

- Python 3.11
- Flask — web interface
- NLTK — text preprocessing
- PyGithub — GitHub data collection
- arxiv.py — arXiv data collection
- HTML/CSS — frontend

---

## Project Structure
AI&DEV_Resource_Retrieval_System/
│
├── data_collection.py      # Collects data from GitHub and arXiv APIs
├── preprocessing.py        # Tokenization, stemming, stop word removal
├── index_builder.py        # Builds the inverted index
├── search_engine.py        # TF-IDF ranking and snippet generation
├── app.py                  # Flask web application
├── evaluation.py           # Precision, Recall, F1 evaluation
│
├── corpus.json             # Raw collected documents
├── index.json              # Inverted index
├── evaluation_data.json    # 20 test queries with relevant document IDs
│
└── templates/
├── search.html         # Search page
└── results.html        # Results page

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/AI-Dev-Resource-Retrieval-System.git
cd AI-Dev-Resource-Retrieval-System
```

**2. Install dependencies**
```bash
pip install flask nltk PyGithub arxiv markupsafe
python -m nltk.downloader punkt stopwords
```

**3. Set your GitHub token**
```bash
export GITHUB_TOKEN="your_token_here"
```

**4. Run the pipeline**
```bash
python index_builder.py
python evaluation.py
python app.py
```

**5. Open in browser**
http://localhost:5000

---

## Evaluation Results

The system was evaluated on 20 queries across the AI/ML domain.

| Metric | Score |
|---|---|
| Average Precision | ~0.80 |
| Average Recall | ~0.80 |
| Average F1 Score | ~0.80 |

---

## Team

Built as an academic project for the Information Retrieval course —
Faculty of Computers and Information, AI & IS Department.

---

## Data Sources

- [GitHub API](https://docs.github.com/en/rest)
- [arXiv API](https://arxiv.org/help/api)
