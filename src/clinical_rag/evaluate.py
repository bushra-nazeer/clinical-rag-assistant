"""Retrieval evaluation on the QA set: hit-rate, MRR, and recall @ k."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from .config import Config, load_config
from .corpus import QA_EVAL
from .retriever import build_index

# Non-interactive backend so figures render in headless containers/CI.
matplotlib.use("Agg")


def evaluate(cfg: Config) -> dict:
    retriever = build_index(cfg)
    k = cfg.eval.k
    hits = 0
    rr_total = 0.0
    recalls = []
    per_question = []

    for qa in QA_EVAL:
        retrieved = [r["doc_id"] for r in retriever.retrieve(qa["question"], k)]
        relevant = set(qa["relevant_doc_ids"])
        hit = any(d in relevant for d in retrieved)
        hits += int(hit)
        rr = 0.0
        for rank, doc_id in enumerate(retrieved, 1):
            if doc_id in relevant:
                rr = 1.0 / rank
                break
        rr_total += rr
        recalls.append(len(set(retrieved) & relevant) / len(relevant))
        per_question.append({"question": qa["question"], "hit": hit, "reciprocal_rank": round(rr, 3)})

    n = len(QA_EVAL)
    metrics = {
        "questions": n,
        "hit_rate_at_k": round(hits / n, 4),
        "mrr_at_k": round(rr_total / n, 4),
        "recall_at_k": round(float(np.mean(recalls)), 4),
        "k": k,
    }

    reports = Path(cfg.paths.reports_dir)
    figures = Path(cfg.paths.figures_dir)
    reports.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    (reports / "retrieval_eval.json").write_text(
        json.dumps({"metrics": metrics, "per_question": per_question}, indent=2)
    )

    plt.figure(figsize=(9, 4))
    plt.bar(range(1, n + 1), [q["reciprocal_rank"] for q in per_question], color="#0E7C66")
    plt.xlabel("Question #")
    plt.ylabel("Reciprocal rank")
    plt.ylim(0, 1.05)
    plt.title(f"Retrieval reciprocal rank per question (MRR@{k} = {metrics['mrr_at_k']})")
    plt.tight_layout()
    plt.savefig(figures / "retrieval_rr.png", dpi=120)
    plt.close()

    return metrics


def main() -> None:
    argparse.ArgumentParser(description="Evaluate retrieval.").parse_args()
    cfg = load_config()
    print(json.dumps(evaluate(cfg), indent=2))


if __name__ == "__main__":
    main()
