"""
Configuration and constants for the MovieBox API client.
"""

from typing import Dict

BASE_URL = "https://moviebox.ph"
API_BASE = "https://h5-api.aoneroom.com/wefeed-h5api-bff"

DEFAULT_HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Referer": "https://moviebox.ph/",
    "Origin": "https://moviebox.ph",
    "X-Client-Info": '{"timezone":"Asia/Dhaka"}',
    "X-Request-Lang": "en",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

PLAYER_HEADERS: Dict[str, str] = {
    "User-Agent": DEFAULT_HEADERS["User-Agent"],
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "X-Client-Info": '{"timezone":"Asia/Dhaka"}',
    "X-Source": "",
}

# HTTP client tuning
REQUEST_TIMEOUT = 25
RETRIES = 3
BACKOFF_FACTOR = 0.6  # seconds
