import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_print_success():
    with patch('asyncio.open_connection', new_callable=AsyncMock) as mock_open_connection:
        mock_reader = AsyncMock()
        # Configure the writer mock with synchronous methods for write() and close()
        mock_writer = AsyncMock()
        mock_writer.write = MagicMock()
        mock_writer.close = MagicMock()

        mock_open_connection.return_value = (mock_reader, mock_writer)

        response = client.post("/print", json={"data": "^XA^XZ", "ip": "127.0.0.1", "port": 9100})

        assert response.status_code == 200
        assert response.json() == {"status": "sent", "printer": "127.0.0.1"}
        mock_open_connection.assert_called_once_with("127.0.0.1", 9100)
        mock_writer.write.assert_called_once_with(b'^XA^XZ')
        mock_writer.drain.assert_awaited_once()
        mock_writer.close.assert_called_once()
        mock_writer.wait_closed.assert_awaited_once()


def test_print_timeout():
    with patch('asyncio.open_connection', new_callable=AsyncMock) as mock_open_connection:
        mock_open_connection.side_effect = asyncio.TimeoutError

        response = client.post("/print", json={"data": "^XA^XZ", "ip": "127.0.0.1", "port": 9100})

        assert response.status_code == 408
        assert response.json() == {"detail": "The printer did not respond in time."}


def test_print_network_error():
    with patch('asyncio.open_connection', new_callable=AsyncMock) as mock_open_connection:
        mock_open_connection.side_effect = ConnectionRefusedError("Connection refused")

        response = client.post("/print", json={"data": "^XA^XZ", "ip": "127.0.0.1", "port": 9100})

        assert response.status_code == 500
        assert "Network error: Connection refused" in response.json()["detail"]
