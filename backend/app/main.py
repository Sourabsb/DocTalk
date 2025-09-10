from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets
import datetime
from .routes import upload, chat, download
from .sessions.manager import SessionManager
from .config import GEMINI_API_KEY, AZURE_VISION_ENDPOINT, AZURE_VISION_KEY

app = FastAPI(title="Document Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost:3000",
        "https://doctalk-delta.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_urlsafe(32)
)

session_manager = SessionManager()
app.state.session_manager = session_manager

app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(download.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Document Chat API is running"}

@app.get("/health")
async def health():
    # Check if necessary services are available
    api_status = {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": str(datetime.datetime.now()),
        "services": {
            "gemini": GEMINI_API_KEY is not None,
            "azure_vision": AZURE_VISION_ENDPOINT is not None and AZURE_VISION_KEY is not None
        }
    }
    return api_status
