FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspace

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .

ENV PYTHONPATH=/workspace
ENV MODEL_PATH=/workspace/models/catboost_churn_model.cbm

CMD ["sh", "-c", "uv run dvc pull && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]