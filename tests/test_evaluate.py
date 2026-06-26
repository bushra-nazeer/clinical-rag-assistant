from clinical_rag.config import load_config
from clinical_rag.evaluate import evaluate


def test_retrieval_quality(tmp_path):
    cfg = load_config()
    cfg.paths.index_path = str(tmp_path / "idx.pkl")
    cfg.paths.reports_dir = str(tmp_path / "reports")
    cfg.paths.figures_dir = str(tmp_path / "reports" / "figures")

    metrics = evaluate(cfg)
    # TF-IDF retrieval on this corpus should comfortably clear these bars.
    assert metrics["hit_rate_at_k"] >= 0.8
    assert 0.0 < metrics["mrr_at_k"] <= 1.0
