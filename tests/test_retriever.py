from clinical_rag.retriever import Retriever


def test_retrieves_relevant_document():
    retriever = Retriever().fit()
    results = retriever.retrieve("first-line medication for type 2 diabetes", k=4)
    doc_ids = [r["doc_id"] for r in results]
    assert "DM-MGMT" in doc_ids
    assert all(0.0 <= r["score"] <= 1.0 for r in results)
    assert len(results) == 4
