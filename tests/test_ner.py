from clinical_rag.ner import extract_entities


def test_extracts_conditions_and_meds():
    entities = extract_entities("Patient with type 2 diabetes on metformin and lisinopril.")
    by_text = {e["text"].lower(): e for e in entities}
    assert "type 2 diabetes" in by_text
    assert by_text["type 2 diabetes"]["type"] == "CONDITION"
    assert by_text["type 2 diabetes"]["code"] == "E11.9"
    assert "metformin" in by_text and by_text["metformin"]["type"] == "MEDICATION"
    assert "lisinopril" in by_text


def test_longest_match_wins():
    # "type 2 diabetes" should be captured as one entity, not also "diabetes".
    entities = extract_entities("history of type 2 diabetes")
    texts = [e["text"].lower() for e in entities]
    assert "type 2 diabetes" in texts
    assert "diabetes" not in texts
