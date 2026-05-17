FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspace

# Asılılıqları kopyalayırıq və quraşdırırıq
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Bütün layihəni (və içindəki models/ qovluğunu) imicə kopyalayırıq
COPY . .

# Python-un app qovluğunu tapması üçün mühit dəyişəni
ENV PYTHONPATH=/workspace

# Birbaşa FastAPI tətbiqini başladırıq
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]