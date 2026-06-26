"""FastAPI clinical RAG service: grounded Q&A with citations, entities, and a
PII guardrail."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from ..config import load_config
from ..rag import answer_question
from ..retriever import load_index
from .schemas import AskResponse

cfg = load_config()
_state: dict = {"retriever": None}


def _load() -> None:
    # load_index builds from the in-code corpus if no pickle exists (cheap).
    _state["retriever"] = load_index(cfg)


@asynccontextmanager
async def lifespan(_: FastAPI):
    _load()
    yield


app = FastAPI(title="Clinical RAG Assistant API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    retriever = _state["retriever"]
    return {
        "status": "ok",
        "documents_indexed": len(retriever.docs) if retriever else 0,
        "llm_provider": cfg.llm.provider,
    }


@app.get("/ask", response_model=AskResponse)
def ask(q: str) -> AskResponse:
    if _state["retriever"] is None:
        raise HTTPException(status_code=503, detail="Index not ready.")
    return AskResponse(**answer_question(cfg, _state["retriever"], q))
