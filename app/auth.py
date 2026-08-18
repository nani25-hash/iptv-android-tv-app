"""
Bearer token manager: acquire and refresh guest JWT (from x-user header or cookies).
This centralizes token handling and keeps it concurrency-safe with an asyncio.Lock.
"""

import asyncio
import json
import re
from typing import Optional

import httpx

from .config import API_BASE, DEFAULT_HEADERS, REQUEST_TIMEOUT


class BearerTokenManager:
    def __init__(self):
        self._token: Optional[str] = None
        self._lock = asyncio.Lock()

    async def get_token(self) -> str:
        """Return a cached token or fetch a new guest token from upstream."""
        if self._token:
            return self._token
        # Ensure only one coroutine fetches the token at once
        async with self._lock:
            # Re-check after acquiring lock
            if self._token:
                return self._token
            async with httpx.AsyncClient(follow_redirects=True, timeout=REQUEST_TIMEOUT) as client:
                resp = await client.get(f"{API_BASE}/home?host=moviebox.ph", headers=DEFAULT_HEADERS)
                x_user = resp.headers.get("x-user")
                if x_user:
                    try:
                        self._token = json.loads(x_user).get("token")
                    except Exception:
                        self._token = None
                if not self._token:
                    # fallback: read from set-cookie
                    cookie = resp.headers.get("set-cookie", "")
                    m = re.search(r"token=([^;]+)", cookie)
                    if m:
                        self._token = m.group(1)
            return self._token or ""

    def set_token(self, token: str) -> None:
        self._token = token


# module-level single instance for convenience
token_manager = BearerTokenManager()
