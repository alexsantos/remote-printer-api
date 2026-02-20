# 1. Imagem base oficial do Python
FROM python:3.11-slim

# 2. Instalar o binário do uv a partir da imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Definir o diretório da aplicação
WORKDIR /app

# 4. Copiar os ficheiros de configuração do projeto
# Copiamos o lockfile primeiro para aproveitar a cache do Docker
COPY pyproject.toml uv.lock ./

# 5. Instalar as dependências
# --frozen: Garante que o uv não altere o lockfile
# --no-install-project: Instala apenas as dependências (camada de cache)
RUN uv sync --frozen --no-cache --no-install-project

# 6. Copiar o código fonte
COPY main.py .

# 7. Garantir que o Python usa o ambiente virtual criado pelo uv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 8. Porta padrão do Cloud Run
EXPOSE 8080

# 9. Executar a aplicação (agora o python já aponta para o .venv)
CMD ["python", "main.py"]