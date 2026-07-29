import httpx
from app.core.config import OPEN_METEO_GEOCODING_URL, OPEN_METEO_FORECAST_URL

class CityNotFoundError(Exception):
    pass

async def get_coordinates(city_name: str):
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OPEN_METEO_GEOCODING_URL, params=params)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])
        if not results:
            raise CityNotFoundError()

        first_result = results[0]
        latitude = first_result["latitude"]
        longitude = first_result["longitude"]

    return {"latitude": latitude, "longitude": longitude}


async def get_current_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "temperature_unit": "fahrenheit"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OPEN_METEO_FORECAST_URL, params=params)
        response.raise_for_status()

        data = response.json()
        current = data["current"]
        temperature = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]

    return {"temperature": temperature, "wind_speed": wind_speed}
