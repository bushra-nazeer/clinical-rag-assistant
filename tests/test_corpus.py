from clinical_rag.corpus import CORPUS, QA_EVAL


def test_corpus_non_empty_and_unique_ids():
    ids = [d["doc_id"] for d in CORPUS]
    assert len(CORPUS) >= 10
    assert len(ids) == len(set(ids))
    assert all({"doc_id", "title", "text"} <= set(d) for d in CORPUS)


def test_qa_relevant_ids_exist_in_corpus():
    ids = {d["doc_id"] for d in CORPUS}
    for qa in QA_EVAL:
        assert qa["relevant_doc_ids"]
        assert set(qa["relevant_doc_ids"]) <= ids
