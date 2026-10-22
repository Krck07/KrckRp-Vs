"""
KrckRP - FastAPI Entry Point
This file defines HTTP endpoints (save/load, API routes) 
and WebSocket/SSE endpoints for real-time chat streaming.
"""

from fastapi import FastAPI

app = FastAPI(title="KrckRP Engine", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "KrckRP Engine is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)