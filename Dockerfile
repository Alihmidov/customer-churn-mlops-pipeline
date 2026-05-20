FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspace

ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

ENV PYTHONPATH=/workspace
ENV MODEL_PATH=/workspace/models/catboost_churn_model.cbm

ENV PATH="/workspace/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]