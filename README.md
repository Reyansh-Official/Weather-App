# Weather App Backend

A FastAPI backend for a weather app that fetches live weather data, stores search history, and exposes API endpoints for managing saved weather records.

This project is primarily focused on practicing backend API development with real tools and production-style concepts.

## Overview

The app accepts a city name, gets current weather data from Open-Meteo, and stores weather history in Supabase. It also includes CRUD endpoints for working with saved history records.

Current capabilities:

- Fetch current weather by city
- Store weather searches in Supabase
- Read weather history
- Read one history item by ID
- Create practice history records
- Update history records with PATCH
- Delete history records
- Validate request and response data with Pydantic
- Inject the Supabase client into routes with FastAPI dependencies
- Run integration-style tests with pytest

## Tech Stack

- Python
- FastAPI
- Pydantic
- Supabase
- Open-Meteo API
- httpx
- Uvicorn
- pytest
- uv

## Concepts Practiced

- FastAPI routing
- API routers
- Query parameters
- Path parameters
- JSON request bodies
- Pydantic request and response models
- CRUD API design
- HTTP status codes
- Error handling with `HTTPException`
- CORS middleware
- Environment variable configuration
- External API integration
- Supabase database operations
- Dependency injection with `Depends`
- Integration testing with `TestClient`

## Current Routes

```txt
GET    /                              -> health check
GET    /weather/                      -> fetch weather by city and save it
GET    /weather/history               -> get weather history
GET    /weather/history/{history_id}  -> get one history item
POST   /weather/history               -> create a history item
PATCH  /weather/history/{history_id}  -> update a history item
DELETE /weather/history/{history_id}  -> delete a history item
```

## Project Structure

```txt
app/
  main.py
  core/
    config.py
    database.py
    weather_api.py
  routers/
    weather.py
  schemas/
    weather.py
tests/
  test_connection.py
  test_weather_routes.py
docs/
  learning-progress.md
```

## Setup

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```txt
SUPABASE_URL=your_supabase_url_here
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here
```

Run the API:

```bash
uv run uvicorn app.main:app --reload
```

Open the docs:

```txt
http://127.0.0.1:8000/docs
```

Run tests:

```bash
uv run pytest
```

## Roadmap

Planned backend concepts and features:

- Cleaner service-layer organization
- Improved database error handling
- Duplicate/history behavior
- Unit tests with mocks
- Shared async HTTP client with FastAPI lifespan
- Custom JWT authentication
- OAuth login flow concepts
- Authorization and protected routes
- User-owned weather history
- Redis-backed rate limiting
- Recently viewed cities with Redis
- Background job flow with `202 Accepted`
- API gateway vs app-level responsibility design

## Authentication And System Design Direction

Authentication and authorization are planned future additions.

The intended direction is:

- JWT-based login for custom authentication
- OAuth concepts for third-party login flows
- Protected routes using FastAPI dependencies
- User ownership checks for weather history records
- Redis for user-based rate limits and recent activity
- API gateway or edge layer for infrastructure-level concerns like IP rate limiting, request limits, TLS, and abuse protection

The FastAPI app will focus on application-level rules such as current user loading, ownership checks, roles, permissions, and user-specific limits.

## Future Background Job Pattern

For slower operations, the API may use a `202 Accepted` flow:

```txt
POST /weather/search-jobs       -> returns 202 Accepted with a job ID
GET  /weather/search-jobs/{id}  -> checks job status or result
```

This pattern avoids making the user wait while the backend completes longer-running work. It would likely use a job table plus a background worker or queue system such as Redis Queue, Celery, or Dramatiq.
