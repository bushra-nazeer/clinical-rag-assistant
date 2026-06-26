"""TF-IDF retrieval over the clinical corpus.

A dependency-free, deterministic retriever. The embedding backend is pluggable:
in production this slot would hold transformer embeddings + a vector DB
(FAISS/Chroma/Milvus); the retrieve() interface is identical.
"""

from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import Config, load_config
from .corpus import CORPUS


class Retriever:
    def __init__(self, docs: list[dict] | None = None):
        self.docs = docs if docs is not None else CORPUS
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix = None

    def fit(self):
        texts = [f"{d['title']}. {d['text']}" for d in self.docs]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)
        return self

    def retrieve(self, query: str, k: int = 4) -> list[dict]:
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.matrix).ravel()
        order = sims.argsort()[::-1][:k]
        return [
            {
                "doc_id": self.docs[i]["doc_id"],
                "title": self.docs[i]["title"],
                "text": self.docs[i]["text"],
                "score": float(sims[i]),
            }
            for i in order
        ]


def build_index(cfg: Config) -> Retriever:
    retriever = Retriever().fit()
    path = Path(cfg.paths.index_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Pickle plain data (sklearn/scipy/builtin types), NOT the custom Retriever
    # class, so the index loads under any entrypoint (pytest, uvicorn, `-m`)
    # without a __main__ class-resolution error.
    payload = {"vectorizer": retriever.vectorizer, "matrix": retriever.matrix, "docs": retriever.docs}
    with open(path, "wb") as fh:
        pickle.dump(payload, fh)
    return retriever


def load_index(cfg: Config) -> Retriever:
    path = Path(cfg.paths.index_path)
    if path.exists():
        payload = None
        try:
            with open(path, "rb") as fh:
                payload = pickle.load(fh)
        except Exception:
            payload = None
        if isinstance(payload, dict):
            retriever = Retriever(docs=payload["docs"])
            retriever.vectorizer = payload["vectorizer"]
            retriever.matrix = payload["matrix"]
            return retriever
    # Missing, unreadable, or old-format index -> rebuild from the corpus.
    return build_index(cfg)


def main() -> None:
    argparse.ArgumentParser(description="Build the retrieval index.").parse_args()
    cfg = load_config()
    retriever = build_index(cfg)
    print(f"Indexed {len(retriever.docs)} documents. Example retrieval for 'diabetes treatment':")
    print(json.dumps([r["doc_id"] for r in retriever.retrieve("diabetes treatment", 4)], indent=2))


if __name__ == "__main__":
    main()
