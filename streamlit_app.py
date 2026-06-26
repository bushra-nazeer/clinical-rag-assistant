"""Streamlit demo for the clinical RAG assistant.

Run locally with `streamlit run streamlit_app.py`, or deploy free on Streamlit
Community Cloud by pointing it at this file.
"""

from __future__ import annotations

import streamlit as st

from clinical_rag.config import load_config
from clinical_rag.rag import answer_question
from clinical_rag.retriever import load_index

st.set_page_config(page_title="Clinical RAG Assistant", page_icon="🩺", layout="centered")


@st.cache_resource
def _setup():
    cfg = load_config()
    return cfg, load_index(cfg)


cfg, retriever = _setup()

st.title("Clinical RAG Assistant")
st.caption(
    "Retrieval-augmented clinical Q&A with citations, clinical entity extraction, "
    "and a PII guardrail. Educational demo, not medical advice. Uses no PHI."
)

examples = [
    "What is the first-line treatment for type 2 diabetes?",
    "What blood pressure is considered stage 2 hypertension?",
    "How is asthma controlled long term?",
]
question = st.text_input("Ask a clinical question", value=examples[0])
st.caption("Try: " + "  ·  ".join(examples[1:]))

if question.strip():
    result = answer_question(cfg, retriever, question)

    if result["pii_redacted"]:
        st.warning("PII redacted before processing: " + ", ".join(result["pii_redacted"]))

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")
    for c in result["citations"]:
        st.markdown(f"- **{c['doc_id']}**: {c['title']}  (relevance {c['score']:.3f})")

    if result["entities"]:
        st.subheader("Detected clinical entities")
        st.write(
            "  ·  ".join(
                f"{e['text']} ({e['type']}" + (f", {e['code']}" if e["code"] else "") + ")"
                for e in result["entities"]
            )
        )
