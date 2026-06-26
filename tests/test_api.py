from fastapi.testclient import TestClient

from clinical_rag.api.main import app


def test_health_ok():
    # Context-manager form runs the lifespan startup that loads the index.
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["documents_indexed"] > 0


def test_ask_returns_grounded_answer():
    with TestClient(app) as client:
        response = client.get("/ask", params={"q": "How is asthma controlled long term?"})
        assert response.status_code == 200
        body = response.json()
        assert body["answer"]
        assert len(body["citations"]) >= 1
        assert "ASTHMA" in [c["doc_id"] for c in body["citations"]]
