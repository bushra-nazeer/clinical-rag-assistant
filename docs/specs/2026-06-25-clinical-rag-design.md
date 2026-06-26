# clinical-rag-assistant — Design Spec

- **Date:** 2026-06-25
- **Status:** Approved
- **Portfolio role:** AI/ML + Data Scientist (repo 6 of 6).

## Overview

A retrieval-augmented clinical Q&A assistant: PII redaction → TF-IDF retrieval
over a clinical reference corpus → dictionary NER → grounded answer generation
with citations, behind a FastAPI service. Built dependency-free and offline-
verifiable, with a configurable generation backend (extractive default, or
hosted Claude/OpenAI).

## Resume claims this proves

| Claim | How |
|---|---|
| RAG, retrieval-augmented generation | Full retrieve → ground → generate pipeline with citations |
| NLP, NER, semantic search, embeddings | TF-IDF retrieval + dictionary clinical NER (pluggable for transformers/scispaCy) |
| LLM / prompt engineering / AI agents | Configurable Claude/OpenAI generation over retrieved context, grounded system prompt |
| Clinical decision support / healthcare AI | Clinical corpus, code-mapped entities, citations |
| HIPAA-conscious handling | PII guardrail redacts identifiers before retrieval/LLM |

## Network-aware design

Default backend is fully offline and download-free (TF-IDF + extractive), so the
repo builds and verifies on a constrained connection. Transformer embeddings,
scispaCy/BioBERT NER, and hosted LLMs are documented, lazily-imported optional
extras — the interfaces are identical, so swapping them in is a config change.

## Testing

Unit tests for PII redaction, NER (longest-match), corpus integrity, retrieval
relevance, the end-to-end RAG response (including PII redaction), retrieval
metrics, and the API.

## Deliverable

Verified (tests + a real `make evaluate` retrieval run + an `/ask` response) →
`clinical-rag-assistant.zip`, shipping the built index so `/ask` works out of
the box. Docker canonical runtime; CI runs ruff + pytest.

> Educational/demo only — not medical advice; uses no PHI.
