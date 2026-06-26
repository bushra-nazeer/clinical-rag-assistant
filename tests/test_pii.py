from clinical_rag.pii import detect_pii, redact_pii


def test_redacts_common_identifiers():
    text = "Contact john@example.com or 415-555-0199; SSN 123-45-6789."
    redacted, types = redact_pii(text)
    assert "john@example.com" not in redacted
    assert "123-45-6789" not in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert {"EMAIL", "PHONE", "SSN"} <= set(types)


def test_no_pii_returns_empty():
    redacted, types = redact_pii("What is the first-line treatment for diabetes?")
    assert types == []
    assert detect_pii("no identifiers here") == []
