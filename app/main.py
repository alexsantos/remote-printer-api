import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Remote Printer Cloud Gateway")

# CORS configuration for your web application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class PrintRequest(BaseModel):
    data: str
    ip: str
    port: int = 9100


@app.post("/print")
async def send_to_printer(job: PrintRequest):
    try:
        # Open a TCP connection to the printer on the internal network
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(job.ip, job.port),
            timeout=8.0
        )

        writer.write(job.data.encode('utf-8'))
        await writer.drain()

        writer.close()
        await writer.wait_closed()

        return {"status": "sent", "printer": job.ip}

    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="The printer did not respond in time.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
