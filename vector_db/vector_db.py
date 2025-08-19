import json
import math
import os
from collections import Counter
from typing import Dict, List, Tuple


def tokenize(text: str) -> List[str]:
    """Simple whitespace tokenizer."""
    return text.lower().split()


def compute_tf(text: str) -> Dict[str, float]:
    tokens = tokenize(text)
    counts = Counter(tokens)
    total = len(tokens)
    return {token: count / total for token, count in counts.items()}


def cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    """Compute cosine similarity between two sparse vectors."""
    common = set(v1) & set(v2)
    numerator = sum(v1[t] * v2[t] for t in common)
    sum1 = sum(v ** 2 for v in v1.values())
    sum2 = sum(v ** 2 for v in v2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if denominator == 0:
        return 0.0
    return numerator / denominator


class VectorDatabase:
    def __init__(self, path: str):
        self.path = path
        self.documents: Dict[str, Dict[str, float]] = {}
        self.texts: Dict[str, str] = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.documents = data.get("documents", {})
                self.texts = data.get("texts", {})

    def add_document(self, doc_id: str, text: str) -> None:
        self.texts[doc_id] = text
        self.documents[doc_id] = compute_tf(text)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        q_vec = compute_tf(query)
        scores = [
            (doc_id, cosine_similarity(q_vec, vec))
            for doc_id, vec in self.documents.items()
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"documents": self.documents, "texts": self.texts}, f, indent=2)
