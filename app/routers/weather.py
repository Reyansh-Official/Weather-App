from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.weather import WeatherResponse, WeatherHistoryItem, WeatherCreate, WeatherUpdate
from app.core.database import get_db
from app.core.weather_api import get_coordinates, get_current_weather, CityNotFoundError
import httpx

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/", response_model=WeatherResponse)
async def get_weather(city_name: str = Query(min_length=2, max_length=80)):
    try:
        coordinates = await get_coordinates(city_name)
        weather = await get_current_weather(coordinates["latitude"], coordinates["longitude"])

        temperature = weather["temperature"]
        wind_speed = weather["wind_speed"]
        weather_data = {
            "city_name": city_name,
            "temperature": temperature,
            "wind_speed": wind_speed
        }

        db = get_db()
        db.table("weather_history").insert(weather_data).execute()
        return weather_data

    except CityNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    except httpx.HTTPError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Internal server error")


@router.get("/history", response_model=list[WeatherHistoryItem])
def get_weather_history(limit: int = Query(default=10, ge=1, le=50)):
    db = get_db()
    response_data = db.table("weather_history").select("*").order("created_at", desc=True).limit(limit).execute()

    return response_data.data

@router.get("/history/{history_id}", response_model=WeatherHistoryItem)
def get_weather_history_item(history_id: int):
    db = get_db()
    response = db.table("weather_history").select("*").eq("id", history_id).execute()

    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found")

    return response.data[0]

@router.delete("/history/{history_id}")
def delete_weather_history_item(history_id: int):
    db = get_db()
    response = db.table("weather_history").select("*").eq("id", history_id).execute()
    if response.data:
        db.table("weather_history").delete().eq("id", history_id).execute()
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found")


@router.post("/history", response_model=WeatherHistoryItem, status_code=status.HTTP_201_CREATED)
def create_weather_history(weather_data: WeatherCreate):
    weather_dict = weather_data.model_dump()
    db = get_db()
    response = db.table("weather_history").insert(weather_dict).execute()

    return response.data[0]

@router.patch("/history/{history_id}", response_model=WeatherHistoryItem, status_code=status.HTTP_200_OK)
def update_weather_history(history_id: int, weather_data: WeatherUpdate):
    update_dict = weather_data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid update")

    db = get_db()
    response = db.table("weather_history").update(update_dict).eq("id", history_id).execute()

    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return response.data[0]


