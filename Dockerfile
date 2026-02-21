# 1. Official Python base image
FROM python:3.13-slim

# 2. Install uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Set the application directory
WORKDIR /app

# 4. Install dependencies using bind mounts (no layer bloat, cached by uv)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# 5. Copy source code
COPY app/ ./app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 6. Default port for Cloud Run
EXPOSE 8080

CMD ["uv", "run", "app/main.py"]