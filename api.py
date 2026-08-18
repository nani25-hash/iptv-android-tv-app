"""
Small wrapper to run the FastAPI app directly with uvicorn.
The original api.py was refactored into the `app` package. This file preserves the old entrypoint.
"""

from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
