# Weather App Learning Progress

This document tracks what we have built, what concepts we have learned, where we are currently, and what remains.

## Fresh Chat Instructions

If this project continues in a fresh chat, follow this learning method:

- Do not just write the code for the user.
- Explain the concept first: what it is, why it exists, and where it fits in the app.
- Give one small implementation task at a time.
- Let the user try writing the code.
- When the user says `check`, inspect the relevant files and give focused feedback.
- If the user is stuck, give hints before giving full code.
- Use the existing project structure and patterns.
- Keep the teaching practical and connected to the weather app.
- Use `uv` commands, not plain `pip` or global Python commands.
- Prefer step-by-step learning over rushing into advanced features.

The current next learning topic is **FastAPI dependency injection**, starting with replacing repeated `db = get_db()` calls with `Depends(...)`.

## Current Status

We are building a FastAPI backend for a basic weather app.

The backend currently:

- Accepts a city name.
- Uses Open-Meteo geocoding to convert the city into latitude and longitude.
- Uses Open-Meteo forecast data to get current temperature and wind speed.
- Stores weather searches in Supabase.
- Provides CRUD routes for saved weather history.
- Uses Pydantic schemas for request and response validation.
- Uses CORS middleware for future frontend access.
- Uses environment variables for Supabase credentials.
- Has integration-style tests that pass.

## Current Routes

```txt
GET    /                              -> health/status check
GET    /weather/                      -> get current weather for a city and save it
GET    /weather/history               -> read saved weather history
GET    /weather/history/{history_id}  -> read one saved history item
POST   /weather/history               -> create a practice history item
PATCH  /weather/history/{history_id}  -> update part of a history item
DELETE /weather/history/{history_id}  -> delete a history item
```

Note: `GET /weather/` currently has a side effect because it saves the weather search to Supabase. That works for this learning app, but later we may make the API more REST-style.

## Current Project Structure

```txt
app/
  __init__.py
  main.py
  core/
    __init__.py
    config.py
    database.py
    weather_api.py
  routers/
    __init__.py
    weather.py
  schemas/
    __init__.py
    weather.py
tests/
  __init__.py
  test_connection.py
  test_weather_routes.py
docs/
  learning-progress.md
```

What each part does:

- `app/main.py`: Creates the FastAPI app, adds middleware, and includes routers.
- `app/routers/weather.py`: Holds the weather API endpoints.
- `app/schemas/weather.py`: Holds Pydantic request and response models.
- `app/core/config.py`: Holds environment/config values.
- `app/core/database.py`: Creates the Supabase client.
- `app/core/weather_api.py`: Talks to the external Open-Meteo API.
- `tests/`: Holds automated tests.
- `docs/`: Holds learning notes and project docs.

## Current Schemas

```txt
WeatherResponse
  city_name
  temperature
  wind_speed

WeatherHistoryItem
  id
  created_at
  city_name
  temperature
  wind_speed

WeatherCreate
  city_name
  temperature
  wind_speed

WeatherUpdate
  city_name optional
  temperature optional
  wind_speed optional
```

Important schema lesson:

```txt
Input schema  -> what the client sends
Output schema -> what the API returns
```

Example:

```txt
POST /weather/history
input:  WeatherCreate
output: WeatherHistoryItem
```

## Concepts Learned

### FastAPI Basics

- A FastAPI app is created with `FastAPI()`.
- Routes are functions connected to URLs.
- `@app.get("/")` creates a GET endpoint.
- FastAPI automatically creates docs at `/docs`.

### Routers

- Routers keep endpoints organized.
- Instead of putting every route in `main.py`, we use `APIRouter`.
- `prefix="/weather"` means every route in that router starts with `/weather`.
- `tags=["weather"]` groups endpoints in the Swagger docs.

### Query Parameters

Query parameters come after `?` in the URL.

Example:

```txt
GET /weather/?city_name=Boston
```

This is useful when the value is an input, filter, option, or search value.

### Path Parameters

Path parameters are part of the URL path itself.

Example:

```txt
GET /weather/history/10
```

This is useful when the value identifies one specific resource.

Mental model:

```txt
Path parameter  -> which exact thing?
Query parameter -> what filter or option?
```

### Request Bodies

POST and PATCH usually receive data in the JSON body.

Example:

```json
{
  "city_name": "Austin",
  "temperature": 90,
  "wind_speed": 9
}
```

FastAPI validates that JSON with a Pydantic model before the route logic runs.

### Pydantic Schemas

Schemas define the shape of data.

We use Pydantic models for:

- Request validation.
- Response validation.
- Swagger documentation.
- Clear API contracts.

Important lesson:

```txt
The dict is the actual data.
The Pydantic model is the rulebook for that data.
```

### Supabase

We created a `weather_history` table with fields:

- `id`
- `created_at`
- `city_name`
- `temperature`
- `wind_speed`

We learned:

- `.insert(...)` saves data.
- `.select("*")` reads data.
- `.order(...)` sorts data.
- `.limit(...)` limits how many rows come back.
- `.eq("id", value)` filters rows where a column equals a value.
- `.update(...)` updates rows.
- `.delete(...)` deletes rows.
- `response.data` contains the returned rows.

Important detail:

`response.data` is usually a list because a database query can return zero, one, or many rows.

### CRUD

We completed CRUD for weather history:

```txt
Create -> POST /weather/history
Read   -> GET /weather/history and GET /weather/history/{id}
Update -> PATCH /weather/history/{id}
Delete -> DELETE /weather/history/{id}
```

Key lessons:

- `POST` creates a new resource.
- `GET` reads resources.
- `PATCH` updates only fields that are sent.
- `DELETE` removes a resource.
- `201 Created` is better than `200 OK` for successful create endpoints.
- `404 Not Found` is used when an ID does not exist.
- `400 Bad Request` is used when a PATCH body is empty.

PATCH detail:

```python
model_dump(exclude_unset=True)
```

This prevents fields missing from the PATCH body from being updated to `null`.

Swagger warning:

If Swagger shows this:

```json
{
  "city_name": "string",
  "temperature": 80,
  "wind_speed": 0
}
```

and you only want to update temperature, delete the other fields and send:

```json
{
  "temperature": 80
}
```

### Row Level Security

Supabase Row Level Security can block inserts if the client does not have permission.

We learned:

- The anon key is meant for public/client-safe usage.
- The service role key bypasses RLS.
- The service role key must only live on the backend.
- The service role key should never be exposed to a frontend or committed to GitHub.

### Environment Variables

We moved secrets into `.env`.

We created config management in:

```txt
app/core/config.py
```

This keeps important values in one place instead of scattering them across the app.

We added environment files to `.gitignore`:

```txt
.env
.env.local
.env.*.local
```

We also created `.env.example` for safe placeholder values.

### External APIs

We are using Open-Meteo.

The flow is:

```txt
city name -> geocoding API -> latitude/longitude -> forecast API -> weather data
```

We learned why this parameter exists:

```python
"current": "temperature_2m,wind_speed_10m"
```

It tells Open-Meteo exactly which current weather fields we want back.

### Async Basics

We are already using:

```python
async def
await
httpx.AsyncClient
```

The current flow is still sequential:

```txt
get coordinates first
then get weather
then save to database
```

That is correct because the weather call depends on the coordinates.

Async still helps because while one request is waiting on an external API, FastAPI can work on other requests.

We have not deeply learned `asyncio` yet. That is still coming.

### Error Handling

We added custom error handling for:

- City not found.
- External weather API failure.
- Missing history item.
- Empty PATCH body.

We learned:

- Use `HTTPException` to return proper API errors.
- `404` means the requested thing was not found.
- `400` means the request is malformed or does not make sense.
- `502` can mean an upstream service failed.
- Custom exceptions like `CityNotFoundError` help separate internal app logic from HTTP response logic.

### Middleware

We learned the concept of middleware:

```txt
request -> middleware -> route -> middleware -> response
```

Middleware runs around routes.

We added CORS middleware so a future frontend can call the backend.

We learned:

- CORS is a browser security rule.
- `allow_origins` controls which frontends can call the API.
- `allow_credentials=True` should not be combined casually with wildcard origins.
- Middleware is added before routers because it applies globally to requests handled by the app.

### Testing

We are using `pytest`.

We learned:

- `uv run pytest` runs the test suite.
- `TestClient(app)` lets tests call FastAPI routes.
- `client.get(...)` simulates a GET request.
- `client.post(...)` sends JSON request bodies with `json={...}`.
- `client.patch(...)` tests PATCH endpoints.
- `client.delete(...)` tests DELETE endpoints.
- Status-code assertions prove the HTTP result.
- Response-body assertions prove the endpoint returned the correct data.

Current tests include:

- Home route test.
- Invalid query parameter test.
- Valid city test.
- Supabase connection test.
- CRUD flow test:

```txt
POST create row
GET created row
PATCH created row
DELETE created row
GET deleted row returns 404
```

The tests passed after the CRUD flow was added.

## Git

Git is version control. It lets us save checkpoints of the project over time.

Useful Git concepts to learn next:

- `git status`: See what files changed.
- `git diff`: See exactly what changed.
- `git add`: Stage changes for a commit.
- `git commit`: Save a checkpoint.
- `git log`: View commit history.
- Branches: Work on a feature without mixing it into the main branch immediately.

Important for this project:

- `.env` should never be committed.
- `.env.example` should be committed because it shows what environment variables are needed.
- `.gitignore` tells Git which files to ignore.
- Good commits should be small and meaningful.

Suggested first commit message when ready:

```txt
Set up FastAPI weather backend
```

## Things Remaining To Learn And Build

### Dependency Injection

This is the current next topic.

We need to learn FastAPI dependency injection with `Depends(...)`.

This will help with:

- Getting the database client.
- Loading settings.
- Authentication.
- Protected routes.
- Reusable validation logic.
- Cleaner testing and mocking.

Starting point:

```txt
Current pattern:
db = get_db()

Next pattern:
db is provided by FastAPI as a dependency
```

### Better API Design

Later, we may clean up the current route design.

Current learning-app behavior:

```txt
GET /weather/?city_name=Boston
```

This fetches current weather and saves it to history.

More REST-style future option:

```txt
GET  /weather/current?city_name=Boston -> fetch current weather only
POST /weather/search                   -> search weather and save history
```

### Unit Tests With Mocks

Current tests are integration-style because they touch Supabase and Open-Meteo.

Still need to learn:

- What mocking is.
- Why unit tests should not depend on real external services.
- How to mock `get_db()`.
- How to mock `get_coordinates()` and `get_current_weather()`.

### Deeper Async / Asyncio

We still need to learn:

- What an event loop is.
- What `async def` really returns.
- Why `await` is required.
- When sequential async is correct.
- When `asyncio.gather()` is useful.
- Why sync database calls inside async routes can be a limitation.

### Lifespan and Shared Clients

Right now, our external API helper opens an `httpx.AsyncClient`.

Later, we should learn FastAPI lifespan so we can:

- Create one shared HTTP client when the app starts.
- Reuse that client across requests.
- Close it when the app shuts down.

### Redis

We want to use Redis later for:

- Rate limiting.
- Recently viewed cities.

Redis should be treated as a fast temporary/cache store, while Supabase/Postgres remains the durable database.

### Authentication

We want to learn custom JWT authentication instead of Supabase Auth.

Topics to learn:

- User table.
- Password hashing.
- Login route.
- JWT creation.
- JWT verification.
- Protected routes.
- `Depends(...)` for current-user logic.

### Frontend Integration

A frontend does not exist yet.

Later we need to connect a frontend to the API and use:

- CORS correctly.
- Request bodies.
- Query parameters.
- Error responses.
- Auth headers once JWT is added.

## Suggested Next Step

Continue with **FastAPI dependency injection**.

First practical goal:

```txt
Learn what Depends(...) means and use it to provide the Supabase db client to routes.
```
