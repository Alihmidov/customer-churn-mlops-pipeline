FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspace

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

ENV PYTHONPATH=/workspace

ENV MODEL_PATH=/workspace/models/catboost_churn_model.cbm

CMD ["sh", "-c", "uv run dvc config core.no_scm true && uv run dvc pull --allow-missing && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]