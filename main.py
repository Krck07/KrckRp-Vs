"""
KrckRP - FastAPI Entry Point
This file defines HTTP endpoints (save/load, API routes)
and WebSocket/SSE endpoints for real-time chat streaming.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="KrckRP Engine", version="0.1.0")

# Mount the frontend static files
if os.path.exists("frontend/dist"):
    app.mount("/frontend", StaticFiles(directory="frontend/dist"), name="frontend")
else:
    # Fallback to serving from src directory for development
    app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def root():
    return {"message": "KrckRP Engine is running"}

# Serve the main UI page at /ui
@app.get("/ui")
async def ui():
    # This will be handled by the static file serving above
    return {"message": "Frontend available at /frontend"}

# Route for library view (this would redirect to the frontend)
@app.get("/library")
async def library():
    return {"message": "Library view - world/campaign management"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)