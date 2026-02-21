import asyncio
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Header, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import Annotated

app = FastAPI(title="Remote Printer Cloud Gateway")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your specific domain
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load the API Key from environment variables for security
API_KEY_SECRET = os.getenv("PRINTER_API_KEY")


class PrintRequest(BaseModel):
    data: str
    ip: str
    port: int = 9100

    # No extra fields are permitted.
    model_config = ConfigDict(extra='forbid')


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Never send to the client the details of the pydantic error.

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "The payload is invalid.",
            "type": "validation_error"
        },
    )


# Dependency function to validate the API Key
async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Invalid or missing API Key."
        )
    return x_api_key


@app.post("/print")
async def send_to_printer(job: PrintRequest, auth: str = Depends(verify_api_key)):
    try:
        # Attempt to open a TCP connection to the printer
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(job.ip, job.port),
            timeout=10.0
        )

        # Send data (encoding as utf-8)
        writer.write(job.data.encode('utf-8'))
        await writer.drain()

        # Properly close the connection
        writer.close()
        await writer.wait_closed()

        return {
            "status": "success",
            "message": "Job sent to printer",
            "printer_ip": job.ip
        }

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail="Request Timeout: The printer did not respond in time."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Network Error: {str(e)}"
        )


# Entry point for Cloud Run / Local execution
if __name__ == "__main__":
    # Cloud Run provides the port via the 'PORT' environment variable
    target_port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=target_port)
