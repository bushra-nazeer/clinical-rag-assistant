"""Dictionary-based clinical entity recognition.

A gazetteer of conditions, medications, labs, and vitals (mapped to codes where
applicable). Pluggable for scispaCy / BioBERT in production; this rule-based
version is deterministic and dependency-free.
"""

from __future__ import annotations

import re

CLINICAL_VOCAB: dict[str, tuple[str, str | None]] = {
    "type 2 diabetes": ("CONDITION", "E11.9"),
    "diabetes": ("CONDITION", "E11.9"),
    "hypertension": ("CONDITION", "I10"),
    "high blood pressure": ("CONDITION", "I10"),
    "asthma": ("CONDITION", "J45.909"),
    "hyperlipidemia": ("CONDITION", "E78.5"),
    "urinary tract infection": ("CONDITION", "N39.0"),
    "gerd": ("CONDITION", "K21.9"),
    "anxiety": ("CONDITION", "F41.9"),
    "coronary artery disease": ("CONDITION", "I25.10"),
    "obesity": ("CONDITION", "E66.9"),
    "chest pain": ("CONDITION", "R07.9"),
    "pneumonia": ("CONDITION", "J18.9"),
    "osteoarthritis": ("CONDITION", "M17.9"),
    "sleep apnea": ("CONDITION", "G47.33"),
    "metformin": ("MEDICATION", None),
    "insulin": ("MEDICATION", None),
    "lisinopril": ("MEDICATION", None),
    "atorvastatin": ("MEDICATION", None),
    "albuterol": ("MEDICATION", None),
    "omeprazole": ("MEDICATION", None),
    "sertraline": ("MEDICATION", None),
    "aspirin": ("MEDICATION", None),
    "nitrofurantoin": ("MEDICATION", None),
    "hemoglobin a1c": ("LAB", None),
    "a1c": ("LAB", None),
    "ldl": ("LAB", None),
    "troponin": ("LAB", None),
    "glucose": ("LAB", None),
    "blood pressure": ("VITAL", None),
    "bmi": ("VITAL", None),
}


def extract_entities(text: str) -> list[dict]:
    lowered = text.lower()
    covered = [False] * len(lowered)
    entities = []
    # Longest terms first so "type 2 diabetes" wins over "diabetes".
    for term in sorted(CLINICAL_VOCAB, key=len, reverse=True):
        entity_type, code = CLINICAL_VOCAB[term]
        for match in re.finditer(r"\b" + re.escape(term) + r"\b", lowered):
            start, end = match.start(), match.end()
            if any(covered[start:end]):
                continue
            for i in range(start, end):
                covered[i] = True
            entities.append({"text": text[start:end], "type": entity_type, "code": code, "start": start})
    entities.sort(key=lambda e: e["start"])
    return entities
