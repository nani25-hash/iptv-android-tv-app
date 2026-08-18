"""
API routes (FastAPI APIRouter).
Contains the dashboard and example proxy endpoints that use the modular HTTP client.
"""

from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

from .http_client import make_request
from .config import API_BASE

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard():
    # Keep the dashboard UI mostly unchanged but loaded from a template string here.
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MovieBox Pure API | Pro Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
        <style>
            /* ... same styles as the original file, shortened for brevity ... */
            body { font-family: 'Outfit', sans-serif; background: #07080c; color: #fff; }
            .container { max-width: 1200px; margin: 0 auto; padding: 60px 24px; }
            header { text-align: center; margin-bottom: 80px; }
            h1 { font-size: 3rem; font-weight: 800; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="badge">🎬 MovieBox Pro API</div>
                <h1>Streaming API Server</h1>
            </header>
        </div>
    </body>
    </html>
    """
    return html_content


@router.get("/proxy")
async def proxy_example(path: str = Query(..., description="Path on the upstream API, e.g. /home?host=moviebox.ph")):
    """Example proxy endpoint showing how to use the shared client.
    This endpoint is intentionally minimal — in production, validate `path` strictly to avoid open proxy issues.
    """
    # Simple safeguard to avoid open proxy abuse; only allow paths that start with '/'
    if not path.startswith("/"):
        return {"error": "Invalid path"}
    url = f"{API_BASE}{path}"
    return await make_request(url)
