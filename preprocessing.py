import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    STOP_WORDS = set(stopwords.words("english"))

stemmer = PorterStemmer()

def preprocess(text: str) -> list[str]:
    if not text:
        return []
    tokens = re.findall(r"[a-zA-Z]+", text)
    tokens = [t.lower() for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in STOP_WORDS]
    return [stemmer.stem(t) for t in tokens]