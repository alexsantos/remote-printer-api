# Remote Printer API

A simple FastAPI application to send raw print data to printers on a local network. This acts as a gateway, allowing you to send print jobs from a web application to a printer that is not directly accessible from the public internet.

## Features

- **Send Raw Data**: Send raw command data (like ZPL, EPL, or ESC/POS) to a specified printer IP address.
- **Simple API**: A single `/print` endpoint for all print jobs.
- **Containerized**: Includes a `Dockerfile` for easy deployment.
- **Tested**: Comes with a full suite of tests using `pytest`.

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended)
- Docker (for containerized deployment)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/remote-printer-api.git
    cd remote-printer-api
    ```

2.  **Create a virtual environment and install dependencies:**
    ```sh
    uv venv
    source .venv/bin/activate
    uv pip install -e .
    ```

### Running the Application

To run the development server:

```sh
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Usage

You can send a POST request to the `/print` endpoint with a JSON payload containing the raw data, the printer's IP address, and an optional port.

**Endpoint:** `POST /print`

**Payload:**

```json
{
  "data": "^XA^FO50,50^ADN,36,20^FDHello, Printer!^FS^XZ",
  "ip": "192.168.1.100",
  "port": 9100
}
```

- `data` (str): The raw command data to be sent to the printer.
- `ip` (str): The IP address of the printer.
- `port` (int, optional): The port number for the printer connection (defaults to 9100).

### Client Examples

**Example using `curl`:**

```sh
curl -X POST "http://127.0.0.1:8000/print" \
     -H "Content-Type: application/json" \
     -d '{
           "data": "^XA^FO50,50^ADN,36,20^FDHello, Printer!^FS^XZ",
           "ip": "192.168.1.100"
         }'
```

**Example using Python:**

```python
import requests

url = "http://127.0.0.1:8000/print"
payload = {
    "data": "^XA^FO50,50^ADN,36,20^FDHello, Printer!^FS^XZ",
    "ip": "192.168.1.100"
}

response = requests.post(url, json=payload)

print(response.json())
```

**Example for Web Browsers (JavaScript `fetch`):**

```javascript
const printData = {
  data: "^XA^FO50,50^ADN,36,20^FDHello, Printer!^FS^XZ",
  ip: "192.168.1.100"
};

fetch('http://127.0.0.1:8000/print', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(printData)
})
.then(response => response.json())
.then(result => {
  console.log('Success:', result);
})
.catch(error => {
  console.error('Error:', error);
});
```

**Example for AngularJS:**

```javascript
// In your AngularJS controller
$http.post('http://127.0.0.1:8000/print', {
  data: "^XA^FO50,50^ADN,36,20^FDHello, Printer!^FS^XZ",
  ip: "192.168.1.100"
}).then(function(response) {
  console.log('Success:', response.data);
}, function(error) {
  console.error('Error:', error);
});
```

**Example for Node.js:**

```javascript
const http = require('http');

const printData = JSON.stringify({
  data: "^XA^FO50,50^ADN,36,20^FDHello, Printer!^FS^XZ",
  ip: "192.168.1.100"
});

const options = {
  hostname: '127.0.0.1',
  port: 8000,
  path: '/print',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': printData.length
  }
};

const req = http.request(options, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log('Response:', JSON.parse(data));
  });
});

req.on('error', (error) => {
  console.error('Error:', error);
});

req.write(printData);
req.end();
```

### Running Tests

To run the test suite:

1.  **Install test dependencies:**
    ```sh
    uv pip install -e .[test]
    ```

2.  **Run pytest:**
    ```sh
    pytest
    ```

### Docker Deployment

The project includes a `Dockerfile` for easy containerization.

1.  **Build the Docker image:**
    ```sh
    docker build -t remote-printer-api .
    ```

2.  **Run the Docker container:**
    ```sh
    docker run -d -p 8080:8080 --name remote-printer-container remote-printer-api
    ```

The API will then be accessible on `http://localhost:8080`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
