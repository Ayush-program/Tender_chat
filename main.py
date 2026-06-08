from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn
import os

from app.database import init_db
from app.routers import leads, chat, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("\n╔══════════════════════════════════════════╗")
    print("║   🏛️  TenderPro AI Chatbot Running!      ║")
    print("╠══════════════════════════════════════════╣")
    print("║  Chatbot : http://localhost:8000          ║")
    print("║  Admin   : http://localhost:8000/admin    ║")
    print("║  API Docs: http://localhost:8000/docs     ║")
    print("╚══════════════════════════════════════════╝\n")
    yield

app = FastAPI(
    title="TenderPro AI Chatbot API",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(leads.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@app.get("/admin")
async def serve_admin():
    return FileResponse("static/admin.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
