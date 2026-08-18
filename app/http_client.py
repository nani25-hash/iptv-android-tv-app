"""
HTTP helper with retry, backoff and basic anti-bot detection.
- Uses the BearerTokenManager to attach Authorization headers.
- Detects anti-bot/captcha by inspecting status codes and HTML body content.
- Refreshes token automatically when x-user header is present in responses.
"""

import asyncio
import json
from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException

from .config import DEFAULT_HEADERS, REQUEST_TIMEOUT, RETRIES, BACKOFF_FACTOR
from .auth import token_manager


def _is_antibot_response(resp: httpx.Response, body_text: Optional[str] = None) -> Optional[str]:
    """Return a reason string if the response looks like an anti-bot/challenge page."""
    if resp.status_code in (429, 403):
        return f"Upstream returned status {resp.status_code}"
    ct = resp.headers.get("content-type", "")
    if "text/html" in ct and body_text:
        low = body_text.lower()
        keywords = ["recaptcha", "g-recaptcha", "cloudflare", "cf-challenge", "bot detection", "are you human", "please enable javascript"]
        for kw in keywords:
            if kw in low:
                return f"Detected anti-bot page (keyword: {kw})"
    return None


async def make_request(url: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None, custom_headers: Optional[Dict[str, str]] = None) -> Any:
    token = await token_manager.get_token()
    headers = {
        **DEFAULT_HEADERS,
        **(custom_headers or {}),
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    last_exc: Optional[Exception] = None
    for attempt in range(1, RETRIES + 1):
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=REQUEST_TIMEOUT) as client:
                if method.upper() == "POST":
                    resp = await client.post(url, headers=headers, json=payload)
                else:
                    resp = await client.get(url, headers=headers)

                # update token if upstream provides a new one
                x_user = resp.headers.get("x-user")
                if x_user:
                    try:
                        new_token = json.loads(x_user).get("token")
                        if new_token:
                            token_manager.set_token(new_token)
                    except Exception:
                        pass

                # Anti-bot detection
                try:
                    body_text = (await resp.aread()).decode(errors="ignore") if resp.content is not None else None
                except Exception:
                    body_text = None

                antibot_reason = _is_antibot_response(resp, body_text)
                if antibot_reason:
                    # Provide a clear error so callers can surface it to users or take action.
                    raise HTTPException(status_code=503, detail=f"Anti-bot detected: {antibot_reason}")

                if resp.status_code != 200:
                    raise HTTPException(status_code=502, detail=f"Upstream API error: {resp.status_code}")

                # Try to parse JSON, otherwise return raw text
                ct = resp.headers.get("content-type", "")
                if "application/json" in ct:
                    return resp.json()
                return body_text

        except HTTPException:
            # Propagate FastAPI HTTPExceptions directly
            raise
        except Exception as e:
            last_exc = e
            # exponential backoff before retrying
            if attempt < RETRIES:
                await asyncio.sleep(BACKOFF_FACTOR * (2 ** (attempt - 1)))
                continue
            # out of retries
            raise HTTPException(status_code=502, detail=f"Request failed after {RETRIES} attempts: {str(e)}")

