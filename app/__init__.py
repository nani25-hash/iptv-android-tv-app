from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router as api_router

app = FastAPI(
    title="MovieBox API Pro",
    description="Full Pure REST API for moviebox.ph — Modular refactor",
    version="2.2.0"
)

# Keep permissive CORS for compatibility; restrict in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
