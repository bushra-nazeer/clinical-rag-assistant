"""PII guardrail: detect and redact common identifiers before a query is sent
to retrieval or a hosted LLM (HIPAA-conscious handling)."""

from __future__ import annotations

import re

PII_PATTERNS = {
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "MRN": re.compile(r"\bMRN[:#\s]*\d{6,10}\b", re.IGNORECASE),
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "PHONE": re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "DATE": re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"),
}


def detect_pii(text: str) -> list[dict]:
    found = []
    for label, pattern in PII_PATTERNS.items():
        for match in pattern.finditer(text):
            found.append({"type": label, "value": match.group(), "start": match.start()})
    return found


def redact_pii(text: str) -> tuple[str, list[str]]:
    """Return (redacted_text, sorted list of PII types found)."""
    redacted = text
    types = set()
    for label, pattern in PII_PATTERNS.items():
        if pattern.search(redacted):
            types.add(label)
            redacted = pattern.sub(f"[REDACTED_{label}]", redacted)
    return redacted, sorted(types)
