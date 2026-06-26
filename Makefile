.PHONY: install index ask evaluate serve test lint format clean

install:
	uv venv --python 3.12
	uv pip install -e ".[dev]"

index:
	uv run python -m clinical_rag.retriever

evaluate:
	uv run python -m clinical_rag.evaluate

# Ask a question from the CLI: make ask Q="what is first-line treatment for type 2 diabetes?"
ask:
	uv run python -m clinical_rag.rag "$(Q)"

serve:
	uv run uvicorn clinical_rag.api.main:app --host 0.0.0.0 --port 8000 --reload

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

clean:
	rm -rf models/*.pkl reports/figures .pytest_cache .ruff_cache
