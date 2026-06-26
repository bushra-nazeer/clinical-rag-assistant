from clinical_rag.config import load_config
from clinical_rag.rag import answer_question
from clinical_rag.retriever import Retriever


def test_answer_question_structure_and_pii_redaction():
    cfg = load_config()
    retriever = Retriever().fit()
    query = "For patient SSN 123-45-6789, how is hypertension managed?"
    result = answer_question(cfg, retriever, query)

    assert "123-45-6789" not in result["question"]
    assert "SSN" in result["pii_redacted"]
    assert result["answer"]
    assert len(result["citations"]) == cfg.retriever.top_k
    assert any(e["type"] == "CONDITION" for e in result["entities"])
