# Remote Printer Cloud Gateway 🖨️☁️

This is a lightweight **FastAPI** gateway designed to run on **Google Cloud Run**. It acts as a bridge between web applications and network printers (TCP/IP), allowing you to send raw print commands (like ZPL or ESC/POS) over HTTPS with built-in security.

---

## 🚀 Features

* **FastAPI & Uvicorn**: High-performance asynchronous execution.
* **X-API-Key Security**: Protected by mandatory header validation.
* **Cloud Native**: Optimized for Google Cloud Run dynamic port environment.
* **Modern Python Tooling**: Managed with `uv` for lightning-fast builds and deterministic dependencies.
* **Full Async I/O**: Non-blocking TCP connections using `asyncio`.

---

## 🛠️ Local Setup & Installation

### Prerequisites

Ensure you have uv installed:

    curl -LsSf https://astral.sh/uv/install.sh | sh

### 1. Clone & Prepare

    git clone https://github.com/alexsantos/remote-printer-api.git
    cd remote-printer-api

### 2. Install Dependencies

    uv sync

### 3. Environment Configuration
The application requires an API Key. You must set the `PRINTER_API_KEY` environment variable:

    export PRINTER_API_KEY="your-secret-key-here"

### 4. Run Locally

    uv run python app/main.py

The server will start at `http://localhost:8080`.

---

## 🔒 Security & API Usage

Every request to the `/print` endpoint must include the `X-API-Key` header.

### Request Specification
* **Method**: POST
* **Path**: `/print`
* **Headers**: 
    * `X-API-Key`: <your_secret_key>
    * `Content-Type`: application/json

### Example Payload

    {
      "data": "^XA^FO50,50^A0N,50,50^FDCloud Print Test^FS^XZ",
      "ip": "192.168.1.50",
      "port": 9100
    }

---

## 🧪 Testing

The project includes a robust test suite using `pytest` and `AsyncMock`. It simulates network behavior without requiring a physical printer.

Run the tests:

    uv run pytest -v

The tests validate:
1.  **Authentication**: Blocks requests with missing or invalid keys.
2.  **Logic**: Ensures data is correctly encoded to bytes before transmission.
3.  **Resilience**: Handles connection timeouts and network errors gracefully.

---

## ☁️ Deployment to Google Cloud Run

The provided `Dockerfile` is optimized to use `uv` for building the production container.

### Deploy Command

    gcloud run deploy printer-gateway \
      --source . \
      --region europe-west1 \
      --set-env-vars PRINTER_API_KEY=your-strong-secret-key \
      --allow-unauthenticated

---

## 📂 Project Structure

    .
    ├── app/
    │   ├── __init__.py
    │   └── main.py          # FastAPI application logic
    ├── tests/
    │   └── test_main.py     # Async test suite with Mocking
    ├── Dockerfile           # Multi-stage build using uv
    ├── pyproject.toml       # Modern Python project configuration
    ├── uv.lock              # Dependency lockfile
    └── README.md            # You are here!

---

**Author**: Alexandre Santos (https://github.com/alexsantos)