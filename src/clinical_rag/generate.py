"""Answer generation with a configurable backend.

Default ``extractive`` composes a grounded answer from the retrieved passages
with citations, no external calls. ``anthropic`` / ``openai`` backends are
lazily imported and call a hosted LLM over the retrieved context, falling back
to extractive if the SDK or API key is unavailable.
"""

from __future__ import annotations

from .config import Config

SYSTEM_PROMPT = (
    "You are a clinical reference assistant. Answer ONLY from the provided context "
    "passages and cite their document IDs. If the context is insufficient, say so. "
    "This is general reference information, not medical advice."
)


def _format_context(passages: list[dict]) -> str:
    return "\n\n".join(f"[{p['doc_id']}] {p['title']}: {p['text']}" for p in passages)


def _extractive(passages: list[dict]) -> str:
    if not passages:
        return "No relevant information was found in the knowledge base."
    parts = [passages[0]["text"]]
    if len(passages) > 1 and passages[1]["doc_id"] != passages[0]["doc_id"]:
        parts.append(passages[1]["text"])
    sources = ", ".join(p["doc_id"] for p in passages[:2])
    return " ".join(parts) + f" (Sources: {sources})"


def _anthropic(cfg: Config, query: str, passages: list[dict]) -> str:
    from anthropic import Anthropic

    client = Anthropic()  # reads ANTHROPIC_API_KEY
    message = client.messages.create(
        model=cfg.llm.anthropic_model,
        max_tokens=cfg.llm.max_tokens,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Context:\n{_format_context(passages)}\n\nQuestion: {query}"}
        ],
    )
    return "".join(block.text for block in message.content if getattr(block, "type", None) == "text")


def _openai(cfg: Config, query: str, passages: list[dict]) -> str:
    from openai import OpenAI

    client = OpenAI()  # reads OPENAI_API_KEY
    response = client.chat.completions.create(
        model=cfg.llm.openai_model,
        max_tokens=cfg.llm.max_tokens,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{_format_context(passages)}\n\nQuestion: {query}"},
        ],
    )
    return response.choices[0].message.content


def generate_answer(cfg: Config, query: str, passages: list[dict]) -> str:
    provider = cfg.llm.provider
    if provider in ("anthropic", "openai"):
        try:
            return _anthropic(cfg, query, passages) if provider == "anthropic" else _openai(cfg, query, passages)
        except Exception as exc:
            fallback = _extractive(passages)
            return f"{fallback}\n[note: LLM backend '{provider}' unavailable ({type(exc).__name__}); used extractive fallback]"
    return _extractive(passages)
