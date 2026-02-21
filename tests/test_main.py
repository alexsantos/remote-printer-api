import pytest
import asyncio
import os
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

# 1. Configuração do ambiente antes de carregar o app
@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    # Define a chave que o servidor vai esperar
    monkeypatch.setenv("PRINTER_API_KEY", "test-secret-key")

@pytest.fixture
def client():
    # Import local para garantir que o FastAPI lê o monkeypatch
    from app.main import app
    return TestClient(app)

# --- TESTES DE SUCESSO E ERROS DE REDE ---

def test_print_success(client):
    # Fazemos o patch exatamente onde o asyncio é usado no seu main.py
    with patch('app.main.asyncio.open_connection', new_callable=AsyncMock) as mock_open:
        mock_reader = AsyncMock()
        mock_writer = AsyncMock()
        mock_writer.write = MagicMock()
        mock_writer.close = MagicMock()
        mock_open.return_value = (mock_reader, mock_writer)

        response = client.post(
            "/print",
            json={"data": "^XA^XZ", "ip": "127.0.0.1", "port": 9100},
            headers={"X-API-Key": "test-secret-key"}
        )

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        mock_open.assert_called_once_with("127.0.0.1", 9100)
        mock_writer.write.assert_called_once_with(b'^XA^XZ')

def test_print_timeout(client):
    with patch('app.main.asyncio.open_connection', new_callable=AsyncMock) as mock_open:
        mock_open.side_effect = asyncio.TimeoutError

        response = client.post(
            "/print",
            json={"data": "^XA^XZ", "ip": "127.0.0.1", "port": 9100},
            headers={"X-API-Key": "test-secret-key"}
        )

        assert response.status_code == 408
        assert "Timeout" in response.json()["detail"]

# --- TESTES DE SEGURANÇA (AUTENTICAÇÃO) ---

def test_print_missing_api_key(client):
    """Verifica se o erro 403 ocorre quando não enviamos o header"""
    response = client.post(
        "/print",
        json={"data": "test", "ip": "127.0.0.1", "port": 9100}
        # Sem headers aqui!
    )
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

def test_print_invalid_api_key(client):
    """Verifica se o erro 403 ocorre com uma chave errada"""
    response = client.post(
        "/print",
        json={"data": "test", "ip": "127.0.0.1", "port": 9100},
        headers={"X-API-Key": "wrong-password-123"}
    )
    assert response.status_code == 403