from pydantic import BaseModel
from datetime import datetime

class WeatherResponse(BaseModel):
    city_name: str
    temperature: float
    wind_speed: float

class WeatherHistoryItem(BaseModel):
    id: int
    created_at: datetime
    city_name: str
    temperature: float
    wind_speed: float

class WeatherCreate(BaseModel):
    city_name: str
    temperature: float
    wind_speed: float

class WeatherUpdate(BaseModel):
    city_name: str | None = None
    temperature: float | None = None
    wind_speed: float | None = None
