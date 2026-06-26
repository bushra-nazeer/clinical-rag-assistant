"""Pydantic response models for the RAG API."""

from __future__ import annotations

from pydantic import BaseModel


class Citation(BaseModel):
    doc_id: str
    title: str
    score: float


class Entity(BaseModel):
    text: str
    type: str
    code: str | None = None
    start: int


class AskResponse(BaseModel):
    question: str
    answer: str
    citations: list[Citation]
    entities: list[Entity]
    pii_redacted: list[str]
