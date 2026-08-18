# IPTV Android TV App - Streaming API Integration

A functional streaming server with mobile app API integration capabilities.

## Features

- **RESTful API**: Pure REST API without scraping
- **Token Management**: Auto-acquire and refresh JWT tokens
- **CORS Support**: Full cross-origin resource sharing
- **Async/Await**: High-performance async operations
- **Mobile Integration**: Ready for Android TV app integration

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python api.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Dashboard homepage
- Additional endpoints for streaming functionality (in development)

## Configuration

Default headers and authentication are pre-configured for the MovieBox API.

## Mobile App Integration

The API is designed to work seamlessly with mobile applications:

- **Authentication**: Bearer token-based authentication
- **Headers**: Mobile-friendly headers included
- **CORS**: Enabled for all origins
- **Content-Type**: JSON responses

## Tech Stack

- FastAPI
- HTTPX (async HTTP client)
- Uvicorn (ASGI server)
- Python 3.8+
