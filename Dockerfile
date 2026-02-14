FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Instala as dependências primeiro (aproveita a cache do Docker)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .

# Executa o uvicorn através do ambiente virtual criado pelo uv
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]