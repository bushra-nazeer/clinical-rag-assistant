"""End-to-end RAG: PII redaction -> retrieval -> NER -> grounded generation."""

from __future__ import annotations

import argparse
import json

from .config import Config, load_config
from .generate import generate_answer
from .ner import extract_entities
from .pii import redact_pii
from .retriever import load_index


def answer_question(cfg: Config, retriever, query: str) -> dict:
    safe_query, pii_types = redact_pii(query)
    passages = retriever.retrieve(safe_query, cfg.retriever.top_k)
    entities = extract_entities(safe_query)
    answer = generate_answer(cfg, safe_query, passages)
    return {
        "question": safe_query,
        "answer": answer,
        "citations": [
            {"doc_id": p["doc_id"], "title": p["title"], "score": round(p["score"], 4)}
            for p in passages
        ],
        "entities": entities,
        "pii_redacted": pii_types,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the clinical RAG assistant.")
    parser.add_argument("question", nargs="*", help="Question to answer.")
    args = parser.parse_args()
    query = " ".join(args.question) or "What is the first-line treatment for type 2 diabetes?"
    cfg = load_config()
    retriever = load_index(cfg)
    print(json.dumps(answer_question(cfg, retriever, query), indent=2))


if __name__ == "__main__":
    main()
