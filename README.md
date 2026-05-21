# 🔍 AI & Dev Resource Retrieval System

> A domain-specific Information Retrieval (IR) system for searching AI and Machine Learning resources across GitHub repositories and arXiv research papers.

Built from scratch using **Python**, with a local corpus, inverted index, TF-IDF ranking, and a **Flask**-based web interface.

---

## 📌 Overview

This project allows users to search a locally stored collection of AI/ML documents and retrieve the most relevant results with highlighted snippets and direct source links.

The system follows a **classical Information Retrieval pipeline**:

1. **Data Collection** — from GitHub and arXiv APIs
2. **Text Preprocessing** — tokenization, normalization, stop-word removal, and stemming
3. **Index Construction** — using an inverted index
4. **Ranking** — using TF-IDF scoring
5. **Web Interface** — using Flask
6. **Evaluation** — using Precision, Recall, and F1 Score

---

## ❓ Problem Statement

Finding relevant AI and Machine Learning resources online can be time-consuming, especially when results are spread across repositories and research papers.

This project addresses that problem by building a **local IR system** that searches across:

- 🗂️ GitHub repositories
- 📄 arXiv research papers

The goal is to return the most relevant documents **quickly and efficiently** using classical IR techniques.

---

## ✨ Features

Given a query such as:

```
deep learning python
```

The system searches through a local corpus of approximately **2,000 documents**, ranks them by relevance, and returns:

- ✅ Relevant GitHub repositories
- ✅ Relevant arXiv papers
- ✅ Highlighted query-term snippets
- ✅ Direct links to original sources

---

## 🏗️ System Architecture

### Main Modules

| File | Responsibility |
|------|----------------|
| `data_collection.py` | Collects data from GitHub and arXiv APIs and saves the corpus |
| `preprocessing.py` | Tokenization, normalization, stop-word removal, and stemming |
| `index_builder.py` | Builds the inverted index and stores it in `index.json` |
| `search_engine.py` | Query preprocessing, TF-IDF ranking, and snippet generation |
| `app.py` | Flask web application |
| `evaluation.py` | Computes Precision, Recall, and F1 Score |

### Web Pages

| File | Description |
|------|-------------|
| `search.html` | Search input page |
| `results.html` | Ranked results display page |

---

## 📦 Data Collection

The corpus was collected from real-world public sources using API requests:

- **GitHub API** — for AI/ML repositories
- **arXiv API** — for research papers in AI/ML

### Document Types Collected

**GitHub Repositories:**
- Repository name
- Description
- README content
- Topic tags

**arXiv Papers:**
- Paper title
- Abstract

> All collected documents are stored locally in `corpus.json`.

---

## ⚙️ Preprocessing Pipeline

Each document is processed before indexing through the following steps:

| Step | Description |
|------|-------------|
| **Tokenization** | Extracts individual terms from raw text |
| **Normalization** | Converts to lowercase, removes non-alphabetic characters |
| **Stop-Word Removal** | Removes common words (e.g., *the*, *is*, *and*) |
| **Stemming** | Reduces words to their root form using Porter Stemmer |

> The **same pipeline** is applied to user queries at search time.

---

## 🔎 Indexing & Retrieval

### Inverted Index

The system builds an inverted index mapping each term to the documents that contain it. The index stores:

- Term frequency
- Document frequency
- Document metadata
- Snippets for result display

> The index is serialized and stored in `index.json`.

### Ranking

Documents are ranked using **TF-IDF scoring**. Query terms are matched against the index and results are sorted by relevance score.

### Snippet Generation

For each result, the system extracts a short snippet centered around the **first occurrence** of a query term. Matching terms are **highlighted** in the results page.

---

## 📊 Evaluation

The system was evaluated using **20 manually designed test queries** that simulate realistic user searches.

### Average Results

| Metric | Score |
|--------|-------|
| **Precision** | 0.500 |
| **Recall** | 1.000 |
| **F1 Score** | 0.667 |

### Interpretation

- **Precision = 0.50** → On average, 5 out of 10 returned documents were relevant.
- **Recall = 1.00** → The system retrieved **all** predefined relevant documents for each query.
- **F1 Score = 0.67** → Reflects the harmonic balance between precision and recall.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A GitHub Personal Access Token

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Dev-Resource-Retrieval-System.git
cd AI-Dev-Resource-Retrieval-System
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install flask nltk PyGithub arxiv markupsafe
python -m nltk.downloader punkt stopwords
```

### 4. Set Your GitHub Token

```bash
export GITHUB_TOKEN="your_token_here"
```

### 5. Run the Pipeline

```bash
python data_collection.py   # Collect corpus (run once)
python index_builder.py     # Build the index
python evaluation.py        # Run evaluation (optional)
python app.py               # Start the web app
```

### 6. Open the Application

Navigate to: [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure

```
AI&DEV_Resource_Retrieval_System/
├── data_collection.py       # GitHub & arXiv data fetching
├── preprocessing.py         # Text cleaning pipeline
├── index_builder.py         # Inverted index construction
├── search_engine.py         # TF-IDF ranking & snippet generation
├── app.py                   # Flask web application
├── evaluation.py            # IR evaluation metrics
├── corpus.json              # Raw collected documents
├── index.json               # Serialized inverted index
├── evaluation_data.json     # Test queries & relevant doc IDs
└── templates/
    ├── search.html          # Search page
    └── results.html         # Results page
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Core language |
| Flask | Web interface |
| NLTK | Text preprocessing |
| PyGithub | GitHub API client |
| arxiv | arXiv API client |
| HTML / CSS | Frontend templates |

---

## ⚠️ Limitations & Future Work

### Current Limitations

- Corpus is **static** and stored locally (no real-time updates)
- Retrieval is **lexical** — no semantic understanding
- Semantic/vector search is not included
- Non-English content is not the primary focus
- Results depend heavily on the quality of the collected corpus

### Planned Improvements

- [ ] BM25 ranking algorithm
- [ ] Semantic search using embeddings or language models
- [ ] Incremental index updates
- [ ] Language detection support
- [ ] Larger and more diverse corpus
- [ ] Better evaluation benchmarks

---


## 📚 References

- Manning, C. D., Raghavan, P., & Schütze, H. — *Introduction to Information Retrieval*
- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [arXiv API Documentation](https://arxiv.org/help/api/)
- [NLTK Documentation](https://www.nltk.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [arxiv.py Documentation](https://github.com/lukasschwab/arxiv.py)

---

> 📝 **Academic Note:** This project was submitted as part of the practical requirements for the **Information Retrieval** course at **October 6 University**, Faculty of Information Systems and Computer Science.
