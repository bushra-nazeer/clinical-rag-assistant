# Multi-stage build.
#   --target dev      -> dev image with test deps (CI-style verification)
#   (default/runtime) -> slim image that serves the FastAPI app
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=120
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

FROM base AS dev
RUN --mount=type=cache,target=/root/.cache/pip pip install --retries 8 -e ".[dev]"
COPY . .
CMD ["pytest", "-q"]

FROM base AS runtime
RUN --mount=type=cache,target=/root/.cache/pip pip install --retries 8 .
COPY config ./config
COPY models ./models
EXPOSE 8000
CMD ["uvicorn", "clinical_rag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
